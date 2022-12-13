import { createStore } from 'redux';
import { PAGES_TYPE } from '../Constants/Pages'

const setPage = "SET_PAGE";
const setChoosedFiles = "SET_CHOOSED_FILES";

let initialState = {
    ui: {
        page: PAGES_TYPE.LOAD_FILES
    },
    data: {
        files: []
    }
}

export const storeActions = {

    setPage: (page) => async (dispatch) => {
        dispatch({
            type: setPage,
            payload: {
                page
            }
        });
    },

    setChoosedFiles: (files) => async (dispatch) => {
        dispatch({
            type: setChoosedFiles,
            payload: {
                files
            }
        })
    }
}


export const reducer = (state = initialState, action) => {
    switch (action.type) {
        case setPage: {
            const { page } = action.payload;
            return {
                ...state,
                ui: {
                    ...state.ui,
                    page: page
                }
            }
        }
        case setChoosedFiles: {
            const { files } = action.payload;
            return {
                ...state,
                data: {
                    ...state.data,
                    files: [...files]
                }
            }
        }
        default:
            return state;

    }
}

