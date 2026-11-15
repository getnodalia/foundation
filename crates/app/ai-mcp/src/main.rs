//! Entry point for the Craft AI MCP bridge; the command line itself is [`nodalia_ai_mcp::cli`].

#![deny(
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::panic,
    clippy::unimplemented,
    clippy::todo,
    clippy::unreachable
)]

use std::process::ExitCode;

fn main() -> ExitCode {
    nodalia_ai_mcp::cli::main(std::env::args().skip(1).collect())
}
