import * as React from "react";
import Snackbar from "@mui/material/Snackbar";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import axios from "axios";
import { API_URL } from "../constants";
import { useEffect, useState } from "react";

export default function SimpleSnackbar() {
  const [open, setOpen] = React.useState(false);

  const handleClick = () => {
    setOpen(true);
  };

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get(API_URL + "/notification/sharing_notification", {
          headers: {
            Authorization: "Bearer " + sessionStorage.id_token,
          },
        })
        .then((response) => {
          if (response.data.length > 0) {
            setOpen(true);
            response.data.forEach((item) => {
              console.log(item);
              axios.patch(
                API_URL + "/notification/sharing_notification/",
                {},
                {
                  params: {
                    file_id: item.file_id,
                  },
                  headers: {
                    Authorization: "Bearer " + sessionStorage.id_token,
                  },
                },
              );
            });
          }
        });
    }, 5000);

    // Clear the interval on unmount
    return () => clearInterval(intervalId);
  }, []);

  const handleClose = (
    event: React.SyntheticEvent | Event,
    reason?: string,
  ) => {
    if (reason === "clickaway") {
      return;
    }

    setOpen(false);
  };

  const action = (
    <React.Fragment>
      <IconButton
        size="small"
        aria-label="close"
        color="inherit"
        onClick={handleClose}
      >
        <CloseIcon fontSize="small" />
      </IconButton>
    </React.Fragment>
  );

  return (
    <div>
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        open={open}
        autoHideDuration={10000}
        onClose={handleClose}
        message="A file has been shared with you! Navigate to shared files to view."
        action={action}
      />
    </div>
  );
}
