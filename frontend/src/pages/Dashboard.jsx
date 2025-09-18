import React from "react";
import http from "../http";
import {
  Paper,
  Typography,
  Grid,
  List,
  ListItem,
  ListItemText,
  Button,
} from "@mui/material";
import { useMutation, useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const { data, refetch } = useQuery({
    queryFn: () => http.get("/api/dashboard/").then((r) => r.data),
    queryKey: ["dashboard"],
  });

  const { mutate } = useMutation({
    mutationFn: ({ item_id }) =>
      http.post("/api/favorites/remove/", { item_id }),
    onSuccess: () => refetch(),
  });

  const handleDelete = (id) => {
    mutate({
      item_id: id,
    });
  };

  const population = data?.population;
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h5" gutterBottom>
          Dashboard
        </Typography>
      </Grid>
      {population && (
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              Online Now
            </Typography>
            <Typography>Online: {population.num_online}</Typography>
            <Typography>Lobby: {population.num_lobby}</Typography>
            <Typography>Dungeon: {population.num_dungeon}</Typography>
          </Paper>
        </Grid>
      )}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            Your Favorites
          </Typography>
          {(!data?.favorites || data.favorites.length === 0) && (
            <Typography color="text.secondary">No favorites yet.</Typography>
          )}
          {!!data?.favorites?.length && (
            <List dense>
              {data.favorites.map((f) => (
                <ListItem
                  key={f.id}
                  divider
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <Link to={`items/${f.item.id}`}>
                    <ListItemText
                      primary={`${f.item.name} (${f.item.rarity})`}
                      secondary={
                        f.latest_price?.price ? `${f.latest_price.price}g` : "—"
                      }
                    />
                  </Link>
                  <Button
                    color="secondary"
                    onClick={() => handleDelete(f.item.id)}
                  >
                    Unfavorite
                  </Button>
                </ListItem>
              ))}
            </List>
          )}
        </Paper>
      </Grid>
    </Grid>
  );
}
