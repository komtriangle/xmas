import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { TagCloud } from 'react-tagcloud';


function WordCloud(props) {

    const [goodWords, setGoodWords] = useState([]);

    useEffect(() => {

        let docs = require(`http://85.192.34.254:8888/UploadDocs/GetJsonByName?name=3e5e5e82-2321-4c7d-85c8-be39244fa2ad-Указатели (подробно)`)
            .then((response) => response.json())
            .then((responseJson) => {
                console.log(responseJson)
                const predictedClass = responseJson.predicted_class;
                const predictedClassInfo = responseJson.outputs_for_class[predictedClass];
                const predicedClassGoodWords = predictedClassInfo.tfidf_top_good.map(word => {
                    return {
                        value: word[0],
                        count: Math.floor(word[1] * 100)
                    }
                })
                setGoodWords([...predicedClassGoodWords]);
            })


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