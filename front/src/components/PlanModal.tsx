import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { Dialog, DialogContentText } from "@mui/material";
import SettingsRoundedIcon from "@mui/icons-material/SettingsRounded";
import { DialogActions, DialogContent, DialogTitle } from "@mui/joy";

export default function PlanModal({ open, onClose, onClickSettings }) {
  return (
    <React.Fragment>
      <Dialog
        open={open}
        onClose={onClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={{ margin: "16px" }}>
          <DialogTitle id="modal-modal-title" variant="h6" component="h2">
            Storage limit exceeded.
          </DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              Navigate to settings to upgrade plan.
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button
              autoFocus
              onClick={() => {
                onClickSettings();
                onClose();
              }}
            >
              Settings
            </Button>
            <Button autoFocus onClick={onClose}>
              Cancel
            </Button>
          </DialogActions>
        </Box>
      </Dialog>
    </React.Fragment>
  );
}
