import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { TagCloud } from 'react-tagcloud';


function WordCloud(props) {

    const [goodWords, setGoodWords] = useState([]);

    useEffect(() => {

        let docs = require(removeExtension(`/documents/${props.fileName}).json`));

        const predictedClass = docs.predicted_class;
        const predictedClassInfo = docs.outputs_for_class[predictedClass];
        const predicedClassGoodWords = predictedClassInfo.tfidf_top_good.map(word => {
            return {
                value: word[0],
                count: Math.floor(word[1] * 100)
            }
        })
        setGoodWords([...predicedClassGoodWords]);
    }, [])

    return (
        <div>
            <TagCloud
                minSize={12}
                maxSize={35}
                tags={goodWords}
            />
        </div>
    )

}

WordCloud.propTypes = {
    fileName: PropTypes.string
}

function removeExtension(filename) {
    return filename.substring(0, filename.lastIndexOf('.')) || filename;
}

export default WordCloud;