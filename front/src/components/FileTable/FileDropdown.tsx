import Dropdown from "@mui/joy/Dropdown";
import MenuButton from "@mui/joy/MenuButton";
import IconButton from "@mui/joy/IconButton";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import Menu from "@mui/joy/Menu";
import MenuItem from "@mui/joy/MenuItem";
import RenameIcon from "@mui/icons-material/DriveFileRenameOutlineRounded";
import ShareIcon from "@mui/icons-material/ShareRounded";
import DeleteIcon from "@mui/icons-material/DeleteRounded";
import * as React from "react";
import DownloadIcon from "@mui/icons-material/Download";

function FileDropdown({
  setDialog,
  isShared,
  onStartRename,
  onDelete,
  onDownload,
  onShare,
}) {
  return (
    <Dropdown>
      <MenuButton
        variant="plain"
        size="sm"
        sx={{
          maxWidth: "32px",
          maxHeight: "32px",
        }}
      >
        <IconButton component="span" variant="plain" color="neutral" size="sm">
          <MoreVertIcon />
        </IconButton>
      </MenuButton>
      <Menu
        placement="bottom-end"
        size="sm"
        sx={{
          zIndex: "99999",
          p: 1,
          gap: 1,
          "--ListItem-radius": "var(--joy-radius-sm)",
        }}
      >
        <MenuItem onClick={onDownload}>
          <DownloadIcon />
          Download
        </MenuItem>
        <MenuItem onClick={onStartRename}>
          <RenameIcon />
          Rename
        </MenuItem>
        {!isShared && (
          <MenuItem
            onClick={() => {
              setDialog(true);
              onShare();
            }}
          >
            <ShareIcon />
            Share
          </MenuItem>
        )}
        {!isShared && (
          <MenuItem onClick={onDelete} sx={{ textColor: "danger.500" }}>
            <DeleteIcon />
            Delete
          </MenuItem>
        )}
      </Menu>
    </Dropdown>
  );
}

export default FileDropdown;
