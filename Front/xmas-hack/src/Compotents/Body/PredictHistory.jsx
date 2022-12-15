import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import LoadedFile from "./LoadedFile";

function PredictHistory(props) {

    let [files, setFiles] = useState([])

    useEffect(() => {
        // React advises to declare the async function directly inside useEffect
        async function loadFiles() {
            try {
                const files = await axios.get("http://85.192.34.254:8888/UploadDocs/GetAllFiles");
                console.log(files["data"])
                setFiles(files["data"])
            } catch (ex) {
                console.log(ex);
            }
        }

        loadFiles();
    }, []);


    return (<div>

        <div>
            {files.map(file => (
                <a href={"http://85.192.34.254:8005/" + file.filePath}>
                    <LoadedFile
                        fileName={file.fileName}
                        fileWeigth={0} />
                </a>
            ))}
        </div>
    </div>)
}

export default PredictHistory;