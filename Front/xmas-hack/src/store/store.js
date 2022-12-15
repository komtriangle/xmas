import { act } from 'react-dom/test-utils';
import { createStore } from 'redux';
import { PAGES_TYPE } from '../Constants/Pages'

const setPage = "SET_PAGE";
const setChoosedFiles = "SET_CHOOSED_FILES";
const setSpinnerStatus = "SET_SPINNER_STATUS";

let initialState = {
    ui: {
        page: PAGES_TYPE.LOAD_FILES,
        spinner: false
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
    },

    setSpinnerStatus: (status) => async (dispatch) => {
        dispatch({
            type: setSpinnerStatus,
            payload: {
                status
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
        case setSpinnerStatus: {
            const { status } = action.payload;
            return {
                ...state,
                ui: {
                    ...state.ui,
                    spinner: status
                }
            }
        }
        default:
            return state;

    }
}

