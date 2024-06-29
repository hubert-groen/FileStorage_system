import * as React from "react";
import { useColorScheme } from "@mui/joy/styles";
import Box from "@mui/joy/Box";
import Typography from "@mui/joy/Typography";
import IconButton from "@mui/joy/IconButton";
import AccountIcon from "@mui/icons-material/AccountCircleOutlined";
import Tooltip from "@mui/joy/Tooltip";
import Dropdown from "@mui/joy/Dropdown";
import Menu from "@mui/joy/Menu";
import MenuButton from "@mui/joy/MenuButton";
import MenuItem from "@mui/joy/MenuItem";
import ListDivider from "@mui/joy/ListDivider";
import DarkModeRoundedIcon from "@mui/icons-material/DarkModeRounded";
import LightModeRoundedIcon from "@mui/icons-material/LightModeRounded";
import SettingsRoundedIcon from "@mui/icons-material/SettingsRounded";
import LogoutRoundedIcon from "@mui/icons-material/LogoutRounded";
import { Avatar } from "@mui/joy";

function ColorSchemeToggle() {
  const { mode, setMode } = useColorScheme();
  const [mounted, setMounted] = React.useState(false);
  React.useEffect(() => {
    setMounted(true);
  }, []);
  if (!mounted) {
    return <IconButton size="sm" variant="outlined" color="primary" />;
  }
  return (
    <Tooltip title="Change theme" variant="outlined">
      <IconButton
        id="toggle-mode"
        size="sm"
        variant="plain"
        color="neutral"
        sx={{ alignSelf: "center" }}
        onClick={() => {
          if (mode === "light") {
            setMode("dark");
          } else {
            setMode("light");
          }
        }}
      >
        {mode === "light" ? <DarkModeRoundedIcon /> : <LightModeRoundedIcon />}
      </IconButton>
    </Tooltip>
  );
}

export default function Header({ user, onLogout, onClickSettings }) {
  return (
    <Box
      sx={{
        display: "flex",
        flexGrow: 1,
        justifyContent: "space-between",
      }}
    >
      Eteam Storage
      <Box
        sx={{
          display: "flex",
          flexDirection: "row",
          gap: 1.5,
          alignItems: "center",
        }}
      >
        <ColorSchemeToggle />
        <AccountDropdown
          user={user}
          onLogout={onLogout}
          onClickSettings={onClickSettings}
        />
      </Box>
    </Box>
  );
}

function AccountDropdown({ user, onLogout, onClickSettings }) {
  return (
    <Dropdown>
      <MenuButton
        variant="plain"
        size="sm"
        sx={{ maxWidth: "32px", maxHeight: "32px" }}
      >
        <AccountIcon />
      </MenuButton>
      <Menu
        placement="bottom-end"
        size="sm"
        sx={{
          position: "relative",
          zIndex: "9999999",
          p: 1,
          gap: 1,
        }}
      >
        <MenuItem disabled={true}>
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
            }}
          >
            <Box sx={{ paddingRight: "16px" }}>
              <Avatar src={user.picture}></Avatar>
            </Box>

            <Box>
              <Typography level="title-sm" textColor="text.primary">
                {user.name}
              </Typography>
              <Typography level="body-xs" textColor="text.tertiary">
                {user.email}
              </Typography>
            </Box>
          </Box>
        </MenuItem>
        <ListDivider />
        <MenuItem onClick={onClickSettings}>
          <SettingsRoundedIcon />
          Settings
        </MenuItem>
        <ListDivider />
        <MenuItem onClick={onLogout}>
          <LogoutRoundedIcon />
          Log out
        </MenuItem>
      </Menu>
    </Dropdown>
  );
}
