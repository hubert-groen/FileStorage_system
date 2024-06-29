import * as React from "react";
import Box from "@mui/joy/Box";
import List from "@mui/joy/List";
import ListSubheader from "@mui/joy/ListSubheader";
import ListItem from "@mui/joy/ListItem";
import ListItemButton from "@mui/joy/ListItemButton";
import ListItemDecorator from "@mui/joy/ListItemDecorator";
import ListItemContent from "@mui/joy/ListItemContent";

import FolderRoundedIcon from "@mui/icons-material/FolderRounded";
import ShareRoundedIcon from "@mui/icons-material/ShareRounded";
import DeleteRoundedIcon from "@mui/icons-material/DeleteRounded";
import ShareForm from "./ShareForm";
import axios from "axios";
import { API_URL } from "../constants";

export default function Navigation({ tab, setTab }) {
  return (
    <List size="sm" sx={{ "--ListItem-radius": "8px", "--List-gap": "4px" }}>
      <ListItem nested>
        <ListSubheader sx={{ letterSpacing: "2px", fontWeight: "800" }}>
          Browse
        </ListSubheader>
        <List
          aria-labelledby="nav-list-browse"
          sx={{
            "& .JoyListItemButton-root": { p: "8px" },
          }}
        >
          <ListItem>
            <ListItemButton
              selected={tab === "files"}
              onClick={() => {
                setTab("files");
              }}
            >
              <ListItemDecorator>
                <FolderRoundedIcon fontSize="small" />
              </ListItemDecorator>
              <ListItemContent>My files</ListItemContent>
            </ListItemButton>
          </ListItem>
          <ListItem>
            <ListItemButton
              selected={tab === "shared"}
              onClick={() => {
                setTab("shared");
              }}
            >
              <ListItemDecorator>
                <ShareRoundedIcon fontSize="small" />
              </ListItemDecorator>
              <ListItemContent>Shared files</ListItemContent>
            </ListItemButton>
          </ListItem>
        </List>
      </ListItem>
    </List>
  );
}
