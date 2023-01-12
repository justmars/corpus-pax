# corpus-pax

[sqlpyd](https://github.com/justmars/sqlpyd) tables: generic users, organizations, and articles.

```mermaid
flowchart TB
subgraph dev env
  pax[corpus-pax]
  pax--run setup_pax--->db[(sqlite.db)]
end
subgraph /corpus-entities
  1(members)--github api---pax
  2(orgs)--github api---pax
end
subgraph /lawsql-articles
  3(articles)--github api---pax
end
pax--cloudflare api-->cf(cloudflare images)
```

## Run

```sh
from corpus_pax import setup_pax
setup_pax("x.db")
```

`setup_pax()` is a collection of 3 functions:

1. `add_individuals_from_api()`
2. `add_organizations_from_api()`
3. `add_articles_from_api()`

Since it's hard to correct the m2m tables, `setup_pax()` drops all the tables first, before adding content.

## Prerequisites

Repository | Description
--:|:--
[corpus-entities](https://github.com/justmars/corpus-entities) | yaml-formatted member and org files
[lawsql-articles](https://github.com/justmars/lawsql-articles) | markdown-styled articles with frontmatter

Since data concerning members will be pulled from such repositories, make sure the individual / org fields in [resources.py](corpus_pax/resources.py) match the data pulled from `corpus-entities`.

Each avatar image should be named `avatar.jpeg` so that these can be uploaded to Cloudflare.

## Install

```zsh
poetry add corpus-pax
poetry update
```

## Supply .env

Create an .env file to create/populate the database. See [sample .env](.env.example) highlighting the following variables:

1. Cloudflare `CF_ACCT`
2. Cloudflare `CF_TOKEN`
3. Github `GH_TOKEN`
4. `DB_FILE` (sqlite)

Note the [workflow](.github/workflows/main.yml) where the secrets are included for Github actions. Ensure these are set in the repository's `<url-to-repo>/settings/secrets/actions`, making the proper replacements when the tokens for Cloudflare and Github expire.

### Notes

#### Why Github

The names and profiles of individuals and organizations are stored in Github. These are pulled into the application via an API call requiring the use of a personal access token.

#### Why Cloudflare Images

Individuals and organizations have images stored in Github. To persist and optimize images for the web, I use [Cloudflare Images](https://www.cloudflare.com/products/cloudflare-images/) to take advantage of modern image formats and customizable variants.

#### Why sqlite

The initial data is simple. This database however will be the foundation for a more complicated schema. Sqlite seems a better fit for experimentation and future app use (Android and iOS rely on sqlite).
