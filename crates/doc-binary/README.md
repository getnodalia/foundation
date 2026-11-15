# nodalia-doc-binary

Reader for the Word 97-2003 binary file format (`.doc`, [MS-DOC]) into the `nodalia-wordmodel`
document model. It is Letra's reader, on `nodalia-cfb` for the compound file and
`nodalia-codepage` for 8-bit text.

```rust
// Not a compound file: an error, never a panic.
assert!(nodalia_doc_binary::read(b"not a .doc").is_err());
assert!(!nodalia_doc_binary::is_encrypted(b"not a .doc"));
```

- `read(bytes)`, `read_with_password(bytes, Option<&str>)`, `is_encrypted(bytes)`.
- Text in pieces (8-bit and UTF-16), paragraph and character formatting, styles, lists,
  tables, sections, headers and footers, notes, comments, fields, bookmarks, pictures and
  OfficeArt shapes, document properties.
- XOR obfuscation, RC4 and RC4 CryptoAPI password protection.

There is no writer.

## Limits

Streams (1 GiB each, refused by `nodalia-cfb` before anything is allocated), paragraphs, pieces,
property counts, table nesting and drawing records are capped; the constants are in the source
next to what they bound, and each has a test. Hostile input gives an error or a best-effort
document, never a panic.
