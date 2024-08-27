# ztkn

## What this thing does

Parses a directory of `.md` files, create a network graph of wikilinks using `networkx` and creates an interactive graph in web browser using `pyvis` and `flask`.

## Motivation

Tools such as [foam](https://github.com/foambubble/foambubble.github.io) and amethyst create interactivate graphs but that are highly-integrated features that are difficult to use outside of their respective application ecosystems. This allows you to interact with your second brain, even if you are on neovim, emacs, or helix.

## Installation

Clone repository to `~/` and set the `src.py` to your PATH. 

## How to use

`ztkn ~/path/to/your/vault`

## TODOs

- [x] Add preview of text when hovering over a node
- [ ] When double clicking on a node, open the node's file in a the system's preffered editor of markdown files
- [ ] Add a search bar to search for nodes
- [ ] Advanced metrics for the graph
  - [ ] Centrality of a given node
  - [ ] Betweenness of a given node(s)
