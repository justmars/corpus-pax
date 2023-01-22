---
hide:
  - navigation
  - toc
---
# Rationale

## Why Github

The names and profiles of individuals and organizations are stored in Github. These are pulled into the application via an API call requiring the use of a personal access token.

## Why Cloudflare Images

Individuals and organizations have images stored in Github. To persist and optimize images for the web, I use [Cloudflare Images](https://www.cloudflare.com/products/cloudflare-images/) to take advantage of modern image formats and customizable variants.

## Why sqlite

The initial data is simple. This database however will be the foundation for a more complicated schema. Sqlite seems a better fit for experimentation and future app use (Android and iOS rely on sqlite).
