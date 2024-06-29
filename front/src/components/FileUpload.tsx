import { FileUploader } from "react-drag-drop-files";
import axios from "axios";
import { API_URL } from "../constants";
import { postUpgradePlan } from "./api";
import PlanModal from "./PlanModal";
import { Button } from "@mui/joy";
import { useState } from "react";

function FileUpload({ onRefresh, openDialog }) {
  const [file, setFile] = useState(null);
  const handleChange = (file) => {
    const form = new FormData();
    form.append("file_input", file);
    axios
      .post(API_URL + "/storage/files", form, {
        headers: {
          Authorization: "Bearer " + sessionStorage.id_token,
        },
      })
      .then((res) => {
        onRefresh();
      })
      .catch((error) => {
        if (error.response.status === 413) {
          openDialog();
        }
      });
    setFile(file);
  };
  return <FileUploader handleChange={handleChange} name="file" />;
}

export default FileUpload;
