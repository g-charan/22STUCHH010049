"use client";
import {
  TextField,
  Button,
  Box,
  Typography,
  CircularProgress,
  Alert,
} from "@mui/material";
import React, { useState } from "react";

// Defining the type for the URL parameters to send to the backend
type UrlParams = {
  url: string;
  validity?: number; // Optional as per backend spec
  shortcode?: string; // Optional as per backend spec
};

// Defining the type for the backend response
type ShortenResponse = {
  shortlink: string;
  expiry: string;
};

const Page = () => {
  const [urlData, setUrlData] = useState<UrlParams>({
    url: "",
    validity: 0, // Default to 0, backend will handle default 30 if not provided or 0
    shortcode: "",
  });

  const [loading, setLoading] = useState<boolean>(false);
  const [response, setResponse] = useState<ShortenResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // IMPORTANT: Replace with the actual URL of your Flask backend
  // Ensure Flask is running on this address and port.
  const FLASK_BACKEND_URL = "http://127.0.0.1:5000";

  const handleShortenUrl = async () => {
    setLoading(true);
    setResponse(null); // Clear previous response
    setError(null); // Clear previous error

    // Prepare payload, removing empty optional fields
    const payload: UrlParams = {
      url: urlData.url,
    };
    if (urlData.validity !== undefined && urlData.validity > 0) {
      payload.validity = urlData.validity;
    }
    if (urlData.shortcode && urlData.shortcode.trim() !== "") {
      payload.shortcode = urlData.shortcode.trim();
    }

    try {
      const res = await fetch(`${FLASK_BACKEND_URL}/shorturls`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok) {
        setResponse(data);
      } else {
        // Handle API errors (e.g., 400, 409, 500 from Flask)
        setError(data.message || "An unknown error occurred.");
      }
    } catch (err) {
      console.error("Network or unexpected error:", err);
      setError(
        "Failed to connect to the backend. Is the Flask server running?"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 2,
        p: 3,
        maxWidth: 500,
        mx: "auto",
        mt: 5,
        border: "1px solid #ccc",
        borderRadius: "8px",
        boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
        backgroundColor: "#fff",
      }}
    >
      <Typography variant="h5" component="h1" gutterBottom align="center">
        URL Shortener
      </Typography>

      <TextField
        id="url-input"
        label="Original URL"
        variant="outlined"
        fullWidth
        value={urlData.url}
        onChange={(e) => setUrlData({ ...urlData, url: e.target.value })}
        error={!!error && urlData.url === ""} // Show error if URL is empty on submission attempt
        helperText={!!error && urlData.url === "" ? "URL is required" : ""}
      />
      <TextField
        id="validity-input"
        label="Validity (minutes)"
        variant="outlined"
        fullWidth
        type="number"
        value={urlData.validity}
        onChange={(e) => {
          const value = e.target.value;
          // Allow empty string for user to clear, but convert to 0 for state
          setUrlData({
            ...urlData,
            validity: value === "" ? 0 : parseInt(value) || 0,
          });
        }}
        inputProps={{ min: 0 }} // Prevent negative validity
      />
      <TextField
        id="shortcode-input"
        label="Custom Shortcode (optional)"
        variant="outlined"
        fullWidth
        value={urlData.shortcode}
        onChange={(e) => setUrlData({ ...urlData, shortcode: e.target.value })}
      />

      <Button
        variant="contained"
        color="primary"
        onClick={handleShortenUrl}
        disabled={loading || !urlData.url.trim()} // Disable if loading or URL is empty
        sx={{ mt: 2, py: 1.5, borderRadius: "8px" }}
      >
        {loading ? (
          <CircularProgress size={24} color="inherit" />
        ) : (
          "Shorten URL"
        )}
      </Button>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      {response && (
        <Box
          sx={{
            mt: 2,
            p: 2,
            border: "1px dashed #2196f3",
            borderRadius: "8px",
            backgroundColor: "#e3f2fd",
          }}
        >
          <Typography variant="subtitle1" gutterBottom>
            Shortened URL Created!
          </Typography>
          <Typography variant="body1">
            <strong>Shortlink:</strong>{" "}
            <a
              href={response.shortlink}
              target="_blank"
              rel="noopener noreferrer"
            >
              {response.shortlink}
            </a>
          </Typography>
          <Typography variant="body2" color="text.secondary">
            <strong>Expires:</strong>{" "}
            {new Date(response.expiry).toLocaleString()}
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default Page;
