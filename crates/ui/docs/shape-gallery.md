# Shared Insert Shapes choices and previews

`nodalia_ui::shapes` shares the shape/connector menu and original procedural previews contributed in
[Letra #2142](https://github.com/storytold/wordcraft/pull/2142). It provides semantic preset
identities, default ordering, connector/arrow classification, capability filtering and a menu built
on the existing accessible `IconButton`. This is reusable menu logic as well as painting.

The overlap is concrete: Celdas's [Insert ribbon](https://github.com/storytold/gridcraft/blob/b8771d51fb4da60bd48c13cf313d6d6014dc5e66/crates/ui-egui/src/ribbon.rs#L1534)
offers rectangle, rounded rectangle, ellipse, triangle, line, arrow and text box. Letra also
offers diamond, star, heart and connectors. Each host must filter by what its engine supports;
a preview does not imply import/export or rendering support in that app.

```rust
let chosen = nodalia_ui::shapes::menu(ui, 220.0, font, &button_style,
    |preset| supported_by_this_app(preset),
    |preset| localize(preset.source_label()),
);
if let Some(preset) = chosen {
    // Adapt the semantic choice to this app's insertion operation.
}
```

`ShapePreset::key()` is a stable choice key, not a universal command payload.
The enum is non-exhaustive: capability adapters should reject unknown future presets by default.
Letra maps `StraightArrowConnector` to `kind: "straightConnector", arrow: "end"`; Celdas
must hide it until its own engine supports attachment/routing. An ordinary `Arrow` remains a
different semantic choice. The library does not silently substitute unsupported objects.

Apps own localization, theme, popup lifetime, current document, insertion coordinates, undo and
selection. Additional actions such as New Drawing Canvas remain app-specific menu entries.
`paint_preset` is also available for app-owned gallery layouts. The previews use original path
geometry and no external assets. They are UI icons, not editable document geometry or a shape
rendering engine. Star and heart contours honor `fill` across their full area, including with no
outline; their fixed concave paths use triangle fans around verified interior centers.
Consumer adoption and command adapters are separate work.
