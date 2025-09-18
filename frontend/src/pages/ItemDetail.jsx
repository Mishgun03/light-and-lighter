import React from "react";
import { Link, useParams } from "react-router-dom";
import http from "../http";
import {
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  AreaChart,
  Area,
} from "recharts";
import {
  Paper,
  Typography,
  Stack,
  Button,
  Avatar,
  TableContainer,
  TableHead,
  Table,
  TableCell,
  TableBody,
  TableRow,
} from "@mui/material";
import { useQuery, useQueryClient } from "@tanstack/react-query";

export default function ItemDetail() {
  const { id } = useParams();

  const { data, isLoading } = useQuery({
    queryFn: () => http.get(`/api/items/${id}/`).then((r) => r.data),
    queryKey: ["items", id],
  });
  const { data: market, isLoading: isMarketLoading } = useQuery({
    queryFn: () => http.get(`/api/items/${id}/market/`).then((r) => r.data),
    queryKey: ["items", "market", id],
  });
  const { data: history, isLoading: isHistoryLoading } = useQuery({
    queryFn: () =>
      http
        .get(`/api/items/${id}/history/`, { params: { interval: "1h" } })
        .then((r) => r.data),
    queryKey: ["items", "history", id],
  });

  console.log(data, market, history);

  const queryClient = useQueryClient();

  async function addFavorite() {
    await http
      .post("/api/favorites/", { item_id: id })
      .then(() => {
        queryClient.invalidateQueries(["dashboard"]);
        alert("Added to favorites");
      })
      .catch((e) => alert(`Error: ${e}`));
  }
  async function removeFavorite() {
    await http
      .post("/api/favorites/remove/", { item_id: id })
      .then(() => {
        queryClient.invalidateQueries(["dashboard"]);
        alert("Removed from favorites");
      })
      .catch((e) => alert(`Error: ${e}`));
  }

  if (isLoading || isHistoryLoading || isMarketLoading)
    return <div>Loading...</div>;

  const item = data?.body || data;

  return (
    <Stack spacing={2}>
      <Stack direction="row" spacing={2} alignItems="center">
        <Avatar
          variant="rounded"
          src={`https://api.darkerdb.com/v1/items/${id}/icon`}
          sx={{ width: 56, height: 56 }}
        />
        <div>
          <Typography variant="h5">{item?.name}</Typography>
          <Typography color="text.secondary">Rarity: {item?.rarity}</Typography>
        </div>
      </Stack>
      <Stack direction="row" spacing={1}>
        <Button onClick={addFavorite}>Favorite</Button>
        <Button color="secondary" onClick={removeFavorite}>
          Unfavorite
        </Button>
      </Stack>
      <Paper sx={{ p: 2 }}>
        <Typography variant="subtitle1" gutterBottom>
          Price History
        </Typography>
        <div style={{ height: 280 }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={history?.map((d) => ({
                ...d,
                ts: new Date(d.created_at || d.timestamp).toLocaleString(),
              }))}
            >
              <defs>
                <linearGradient id="colorAvg" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8884d8" stopOpacity={0.5} />
                  <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ts" minTickGap={32} />
              <YAxis />
              <Tooltip />
              <Area
                type="monotone"
                dataKey={history[0]?.price !== undefined ? "price" : "avg"}
                stroke="#8884d8"
                fillOpacity={1}
                fill="url(#colorAvg)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Paper>
      <Paper sx={{ p: 2 }}>
        <Typography variant="subtitle1" gutterBottom>
          Recent Listings
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Created At</TableCell>
                <TableCell>Price</TableCell>
                <TableCell>Quantity</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {market?.body?.map((m) => (
                <TableRow key={m.id}>
                  <TableCell>{m.created_at.toLocaleString()}</TableCell>
                  <TableCell>{m.price}</TableCell>
                  <TableCell>{m.quantity}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Stack>
  );
}

//{new Date(m.created_at).toLocaleString()} — {m.price}g (qty {m.quantity})
