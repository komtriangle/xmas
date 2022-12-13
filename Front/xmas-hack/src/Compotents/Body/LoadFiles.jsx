import React, { useState } from "react";
import { connect } from "react-redux"
import { bindActionCreators } from "redux";
import { storeActions } from "../../store/store"
import axios from "axios";

function LoadFiles(props) {

    const [files, setFiles] = useState([])

    const fileInputOnChange = (files) => {
        setFiles(files)
        var filesToStore = files.map(file => {
            return {
                name: file.name,
                size: Math.round(file.size / 1024)
            }
        })
        props.setChoosedFiles(filesToStore)
    }

    const sendFilesToBack = () => {
        const formData = new FormData();
        files.forEach(file => {
            formData.append("files", file);
        })
        try {
            const res = axios.post("http://85.192.34.254:8888/UploadDocs", formData);
        } catch (ex) {
            console.log(ex);
        }
    }

    return (
        <div className="loadfiles">
            <div className="load-files-instruction">Здесь вы можете определить тип договоров. Для этого вам надо выбрать один или несколько документов
                с вашего компьютера. Допустимые типу файлов: doc, docx, pdf.
            </div>
            <input
                type="file"
                multiple="multiple"
                accept=".doc,.docx,application/pdf, application/msword"
                onChange={e => fileInputOnChange([...e.target.files])} />
            <button
                type='submit'
                onClick={sendFilesToBack}>
                <p>Определить тип</p>
            </button>
        </div>)
}

function mapStateToProps(state) {
    return {
    }
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators({
        setChoosedFiles: storeActions.setChoosedFiles
    }, dispatch)

}

export default connect(mapStateToProps, mapDispatchToProps)(LoadFiles)
