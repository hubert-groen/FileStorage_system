import { useEffect, useState } from "react";
import axios from "axios";
import { API_URL } from "../constants.js";
import Box from "@mui/joy/Box";
import Sheet from "@mui/joy/Sheet";
import FileUpload from "./FileUpload.js";
import FileTable from "./FileTable/FileTable.js";
import * as React from "react";

function SharedFilesPage({ openDialog }) {
  const [files, setFiles] = useState<any>([]);
  const refreshFiles = () => {
    axios
      .get(API_URL + "/storage/shared_files", {
        headers: {
          Authorization: "Bearer " + sessionStorage.id_token,
        },
      })
      .then((res) => {
        console.log(res.data);
        setFiles(res.data);
      });
  };
  useEffect(() => {
    refreshFiles();
  }, []);

  return (
    <Box sx={{ margin: "auto", width: "70vw", justifyContent: "center" }}>
      <Box sx={{ padding: "1rem" }}></Box>
      <Box sx={{ padding: "1rem" }}>
        <Sheet
          variant="outlined"
          sx={{
            justifySelf: "center",
            borderRadius: "sm",
          }}
        >
          <FileTable
            isShared={true}
            files={files}
            refreshFiles={refreshFiles}
          />
        </Sheet>
      </Box>
    </Box>
  );
}
export default SharedFilesPage;
