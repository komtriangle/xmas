import pickle
from enum import Enum
from pathlib import Path
from typing import List, Dict, Tuple
import re

import pandas as pd
import tika
from catboost import CatBoostClassifier, Pool
from sklearn.feature_extraction.text import TfidfVectorizer
from tika import parser
import numpy as np

from pydantic import BaseModel


class Word(BaseModel):
    word: str
    importance: float


class Paragraph(BaseModel):
    words: List[Word]


class ModelOutputForClass(BaseModel):
    tfidf_top_good: List[Tuple[str, float]]
    tfidf_top_bad: List[Tuple[str, float]]
    probability: float


class ModelOutputs(BaseModel):
    task_id: int
    # paragraphs: List[Paragraph]
    predicted_class: str
    outputs_for_class: Dict[str, ModelOutputForClass]


class ModelInputs(BaseModel):
    task_id: int
    doc_path: str


_RE_SPACE = re.compile('\s+')
_RE_UNDER = re.compile('_+')

_N_MODELS = 5
_TARGET_LIST = ['Договоры для акселератора/Договоры купли-продажи',
                'Договоры для акселератора/Договоры оказания услуг',
                'Договоры для акселератора/Договоры аренды',
                'Договоры для акселератора/Договоры подряда',
                'Договоры для акселератора/Договоры поставки']


class Predictor:
    def __init__(self, model_dir: Path):
        tika.initVM()
        ensemble = []
        for i in range(_N_MODELS):
            with (model_dir / 'vectorizer' / f'{i}.pkl').open('rb') as f_io:
                vec = pickle.load(f_io)
            mdl = CatBoostClassifier().load_model(model_dir / 'catboost' / f'{i}.cbm')
            ensemble.append((vec, mdl))
        self._ensemble = ensemble

    def process(self, inputs: ModelInputs) -> ModelOutputs:
        doc = self.preprocess_str(parser.from_file(str(Path('docs') / inputs.doc_path))['content'])
        predicts = []
        importances_all = []
        for i in range(_N_MODELS):
            vec, cb = self._ensemble[i]
            features = vec.transform([doc])
            feature_names = vec.get_feature_names_out()
            cb_pool = Pool(features)
            cb_results = cb.predict_proba(cb_pool)[0]
            cb_importance = cb.get_feature_importance(cb_pool, type='ShapValues')[0, :, :-1]
            importance = pd.DataFrame(data=cb_importance.T, index=feature_names, columns=_TARGET_LIST)
            result = pd.Series(data=cb_results, index=_TARGET_LIST)
            importances_all.append(importance)
            predicts.append(result)
        predicts = pd.concat(predicts).reset_index().groupby('index').mean()[0]
        importances_all = pd.concat(importances_all, axis=0).reset_index().groupby('index').sum()

        out_for_class = {}
        for tgt in _TARGET_LIST:
            proba = predicts[tgt]
            shapley = importances_all[tgt].sort_values()
            shapley_bad = shapley.iloc[:30]
            shapley_good = shapley.iloc[-30:]
            shapley_bad = list(zip(shapley_bad.index, [x.item() for x in shapley_bad.values]))
            shapley_good = list(zip(shapley_good.index, [x.item() for x in shapley_good.values]))
            out_for_class[tgt] = ModelOutputForClass(probability=proba.item(),
                                                     tfidf_top_good=shapley_good[::-1],
                                                     tfidf_top_bad=shapley_bad)
        return ModelOutputs(
            task_id=inputs.task_id,
            predicted_class=predicts.sort_values().index[-1],
            outputs_for_class=out_for_class
        )

    def preprocess_str(self, s: str) -> str:
        s = _RE_SPACE.sub(' ', s)
        s = _RE_UNDER.sub('__', s)
        return s.strip()


if __name__ == '__main__':
    pred = Predictor(Path('./model'))
    res = pred.process(ModelInputs(task_id=0, doc_path='2b25ecf601a9ce0c2a33c8e1d9746df2.doc'))
    print('TOP положительных слов')
    print(*res.outputs_for_class[res.predicted_class].tfidf_top_good, sep='\n')
    print('TOP отрицательных слов')
    print(*res.outputs_for_class[res.predicted_class].tfidf_top_bad, sep='\n')
    # print(res)