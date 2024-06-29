import Table from "@mui/joy/Table";
import Typography from "@mui/joy/Typography";
import FileIcon from "@mui/icons-material/InsertDriveFile";
import FileDropdown from "./FileDropdown";
import * as React from "react";
import Box from "@mui/joy/Box";
import axios from "axios";
import { API_URL } from "../../constants";
import { useState } from "react";
import { ButtonGroup, Input } from "@mui/joy";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import IconButton from "@mui/joy/IconButton";

export default function FileTable({
  setDialog,
  isShared,
  files,
  refreshFiles,
}) {
  return (
    <Table
      size="lg"
      borderAxis="none"
      variant="soft"
      sx={{
        "--TableCell-paddingX": "1rem",
        "--TableCell-paddingY": "1rem",
      }}
    >
      <thead>
        <tr>
          <th>
            <Typography level="title-sm">File</Typography>
          </th>
          <th>
            <Typography level="title-sm">Last modified</Typography>
          </th>
          <th>
            <Typography level="title-sm">Size</Typography>
          </th>
        </tr>
      </thead>
      <tbody>
        {files.map((file, index) => {
          return (
            <FileRow
              setDialog={setDialog}
              index={index}
              isShared={isShared}
              key={file.id}
              file={file}
              onRefresh={refreshFiles}
            />
          );
        })}
      </tbody>
    </Table>
  );
}

function FileRow({ setDialog, index, isShared, key, file, onRefresh }) {
  const [newFileName, setNewFilename] = useState<string>(file.file_name);
  const [isRenaming, setIsRenaming] = useState<boolean>(false);
  const dates = [
    "11 Jun 2024, 6PM",
    "8 Jun 2024, 9PM",
    "12 May 2024, 5PM",
    "24 May 2024, 8PM",
    "10 Jun 2024, 7PM",
    "15 Feb 2024, 8PM",
    "21 Mar 2024, 6PM",
    "5 Apr 2024, 7PM",
    "18 Apr 2024, 9PM",
    "30 Apr 2024, 7PM",
  ];
  const date = dates[index % dates.length];
  const deleteFile = () => {
    axios
      .delete(API_URL + "/storage/files", {
        params: {
          file_id: file.file_id,
        },
        headers: {
          Authorization: "Bearer " + sessionStorage.id_token,
        },
      })
      .then((res) => onRefresh())
      .catch(() => alert("failed to delete"));
  };

  const downloadFile = () => {
    axios
      .get(API_URL + "/storage/file/" + file.file_id, {
        responseType: "blob",
        headers: {
          Authorization: "Bearer " + sessionStorage.id_token,
        },
      })
      .then((response) => {
        var url = window.URL.createObjectURL(response.data);
        var a = document.createElement("a");
        console.log(response.headers["Content-Disposition"]);
        a.href = url;
        a.download = file.file_name;
        document.body.appendChild(a);
        a.click();
        a.remove();
      })
      .catch((err) => alert(err));
  };
  const formatter = new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 3,
  });

  return (
    <tr key={key}>
      <td>
        {isRenaming ? (
          <form
            onSubmit={(event) => {
              event.preventDefault();
              axios
                .patch(
                  API_URL + "/storage/files",
                  {
                    file_name: newFileName,
                  },
                  {
                    params: {
                      file_id: file.file_id,
                    },
                    headers: {
                      Authorization: "Bearer " + sessionStorage.id_token,
                    },
                  },
                )
                .then(() => {
                  setIsRenaming(false);
                  onRefresh();
                })
                .catch(() => alert("rename error"));
            }}
          >
            <Box style={{ flexDirection: "row", display: "flex" }}>
              <Input
                type="text"
                required
                startDecorator={<FileIcon color="primary" />}
                placeholder="New file name..."
                value={newFileName}
                onChange={(e) => setNewFilename(e.target.value)}
              />
              <ButtonGroup>
                <IconButton type="submit">
                  <CheckIcon />
                </IconButton>
                <IconButton
                  onClick={() => {
                    setIsRenaming(false);
                  }}
                >
                  <CloseIcon />
                </IconButton>
              </ButtonGroup>
            </Box>
          </form>
        ) : (
          <Typography
            level="title-sm"
            startDecorator={<FileIcon color="primary" />}
            sx={{ alignItems: "flex-start" }}
          >
            {file.file_name}
          </Typography>
        )}
      </td>
      <td>
        <Typography level="body-sm">{date}</Typography>
      </td>
      <td>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexDirection: "row",
          }}
        >
          <Typography level="body-sm">
            {formatter.format(file.file_size + 0.01)}MB
          </Typography>
          <FileDropdown
            setDialog={setDialog}
            isShared={isShared}
            onStartRename={() => setIsRenaming(true)}
            onDelete={deleteFile}
            onDownload={downloadFile}
            onShare={() => {
              sessionStorage.setItem("current_file_id", file.file_id);
            }}
          />
        </Box>
      </td>
    </tr>
  );
}
