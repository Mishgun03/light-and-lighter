import React, { useEffect, useState } from "react";
import http from "../http";
import { Link, useSearchParams } from "react-router-dom";
import {
  Grid,
  Paper,
  TextField,
  MenuItem,
  Stack,
  Typography,
  Avatar,
  Button,
  CircularProgress,
  Pagination,
} from "@mui/material";
import RarityChip from "../components/RarityChip";
import { useQuery } from "@tanstack/react-query";

export default function Items() {
  const [page, setPage] = useState(1);
  const [searchParams, setSearchParams] = useSearchParams();

  const name = searchParams.get("name") || "";
  const rarity = searchParams.get("rarity") || "";
  const type = searchParams.get("type") || "";
  const slot_type = searchParams.get("slot_type") || "";

  const setQ = (arg) =>
    setSearchParams((searchParams) => {
      arg ? searchParams.set("name", arg) : searchParams.delete("name");
      return searchParams;
    });
  const setRarity = (arg) =>
    setSearchParams((searchParams) => {
      arg ? searchParams.set("rarity", arg) : searchParams.delete("rarity");
      return searchParams;
    });
  const setType = (arg) =>
    setSearchParams((searchParams) => {
      arg ? searchParams.set("type", arg) : searchParams.delete("type");
      return searchParams;
    });
  const setSlot = (arg) =>
    setSearchParams((searchParams) => {
      arg
        ? searchParams.set("slot_type", arg)
        : searchParams.delete("slot_type");
      return searchParams;
    });

  const {
    data,
    fetch,
    isLoading: loading,
  } = useQuery({
    queryFn: () =>
      http
        .get("/api/items/", {
          params: {
            name: name ? name : undefined,
            rarity: rarity ? rarity : undefined,
            type: type ? type : undefined,
            slot_type: slot_type ? slot_type : undefined,
            page: page ? page : undefined,
          },
        })
        .then((r) => r.data),
    queryKey: ["items", { name, rarity, type, slot_type, page }],
  });

  const handleFetchItems = () => {
    fetch();
  };

  const pagination = data?.pagination;
  const pages = pagination?.num_pages;

  return (
    <Stack spacing={2}>
      <Typography variant="h5">Items</Typography>
      <Stack direction={{ xs: "column", sm: "row" }} spacing={1}>
        <TextField
          size="small"
          label="Name"
          value={name}
          onChange={(e) => setQ(e.target.value)}
        />
        <TextField
          size="small"
          label="Rarity"
          value={rarity}
          onChange={(e) => setRarity(e.target.value)}
          select
          sx={{ minWidth: 160 }}
        >
          {[
            "",
            "Poor",
            "Common",
            "Uncommon",
            "Rare",
            "Epic",
            "Legendary",
            "Unique",
            "Artifact",
          ].map((r) => (
            <MenuItem key={r || "any"} value={r}>
              {r || "Any"}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          size="small"
          label="Type"
          value={type}
          onChange={(e) => setType(e.target.value)}
          select
          sx={{ minWidth: 160 }}
        >
          {["", "Accessory", "Armor", "Misc", "Utility", "Weapon"].map((r) => (
            <MenuItem key={r || "any"} value={r}>
              {r || "Any"}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          size="small"
          label="Slot"
          value={slot_type}
          onChange={(e) => setSlot(e.target.value)}
          select
          sx={{ minWidth: 160 }}
        >
          {[
            "",
            "Back",
            "Chest",
            "Foot",
            "Hands",
            "Head",
            "Legs",
            "Necklace",
            "Primary",
            "Ring",
            "Sash",
            "Secondary",
            "Unarmed",
            "Utility",
          ].map((r) => (
            <MenuItem key={r || "any"} value={r}>
              {r || "Any"}
            </MenuItem>
          ))}
        </TextField>
        <Button onClick={handleFetchItems}>Search</Button>
        {loading && <CircularProgress />}
      </Stack>
      <Grid container spacing={2}>
        {data?.body?.map((i) => (
          <Grid item xs={12} sm={6} md={4} key={i.id}>
            <Paper sx={{ p: 2, display: "flex", gap: 1, alignItems: "center" }}>
              <Avatar
                variant="rounded"
                src={`https://api.darkerdb.com/v1/items/${i.id}/icon`}
                sx={{ width: 48, height: 48 }}
              />
              <div>
                <Link to={`/items/${i.id}`}>{i.name}</Link>
                <div>
                  <RarityChip rarity={i.rarity} />
                </div>
              </div>
            </Paper>
          </Grid>
        ))}
      </Grid>
      <Pagination
        count={pages}
        page={page}
        onChange={(event, value) => setPage(value)}
      />
    </Stack>
  );
}
