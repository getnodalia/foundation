//! An app that embeds the writer names itself in `docProps/app.xml` (its own test binary: the
//! name is set once per process).

use std::io::Read;

#[test]
fn the_embedding_app_names_itself_in_app_xml() {
    assert_eq!(nodalia_docx::application_name(), "Letra", "the default");
    nodalia_docx::set_application_name("Example Writer");
    nodalia_docx::set_application_name("Other");
    assert_eq!(nodalia_docx::application_name(), "Example Writer", "only the first call counts");
    let mut d = nodalia_wordmodel::Document::new();
    d.body = vec![nodalia_wordmodel::para_block(nodalia_wordmodel::Paragraph::with_text("Text", Default::default()))];
    let bytes = nodalia_docx::write(&d).unwrap();
    let mut z = zip::ZipArchive::new(std::io::Cursor::new(&bytes)).unwrap();
    let mut app = String::new();
    z.by_name("docProps/app.xml").unwrap().read_to_string(&mut app).unwrap();
    assert!(app.contains("<Application>Example Writer</Application>"), "{app}");
}
