import * as React from "react";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import Card from "@mui/joy/Card";
import CardActions from "@mui/joy/CardActions";
import Chip from "@mui/joy/Chip";
import Divider from "@mui/joy/Divider";
import Typography from "@mui/joy/Typography";
import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";
import { postUpgradePlan } from "./api";

export default function UpgradePlanCards() {
  return (
    <Box
      sx={{
        margin: "auto",
        width: "50%",
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(min(200%, 400px), 2fr))",
        gap: 2,
      }}
    >
      <Card
        size="lg"
        variant="outlined"
        sx={{ gridColumn: "1 / 2", width: 400 }}
      >
        <Chip size="sm" variant="outlined">
          {"10 MB"}
        </Chip>
        <Typography level="h2">Basic</Typography>
        <Divider inset="none" />
        <CardActions>
          <Typography level="title-lg" sx={{ mr: "auto" }}>
            FREE{" "}
          </Typography>
        </CardActions>
      </Card>
      <Card
        size="lg"
        variant="outlined"
        sx={{ gridColumn: "2 / 2", width: 400, bgcolor: "gold" }}
      >
        <Chip size="sm" variant="outlined">
          100 GB
        </Chip>
        <Typography level="h2">Gold</Typography>
        <Divider inset="none" />
        <CardActions>
          <Typography level="title-lg" sx={{ mr: "auto" }}>
            $100{" "}
          </Typography>
          <Button
            variant="soft"
            color="neutral"
            onClick={() => {
              postUpgradePlan("gold");
            }}
            endDecorator={<KeyboardArrowRight />}
          >
            Upgrade now
          </Button>
        </CardActions>
      </Card>
      <Card
        size="lg"
        variant="solid"
        color="neutral"
        sx={{ gridColumn: "1 / 2", width: 400, bgcolor: "silver" }}
      >
        <Chip size="sm" variant="outlined">
          10 GB
        </Chip>
        <Typography level="h2">Silver</Typography>
        <Divider inset="none" />
        <CardActions>
          <Typography level="title-lg" sx={{ mr: "auto" }}>
            $50{" "}
          </Typography>
          <Button
            variant="soft"
            color="neutral"
            onClick={() => {
              postUpgradePlan("silver");
            }}
            endDecorator={<KeyboardArrowRight />}
          >
            Upgrade now
          </Button>
        </CardActions>
      </Card>
      <Card
        size="lg"
        variant="solid"
        color="neutral"
        invertedColors
        sx={{ gridColumn: "2 / 2", width: 400, bgcolor: "neutral.900" }}
      >
        <Chip size="sm" variant="outlined">
          UNLIMITED
        </Chip>
        <Typography level="h2">Unlimited</Typography>
        <Divider inset="none" />
        <CardActions>
          <Typography level="title-lg" sx={{ mr: "auto" }}>
            $200{" "}
          </Typography>
          <Button
            endDecorator={<KeyboardArrowRight />}
            onClick={() => {
              postUpgradePlan("unlimited");
            }}
          >
            Upgrade now
          </Button>
        </CardActions>
      </Card>
    </Box>
  );
}
