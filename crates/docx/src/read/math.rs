//! Office Math (OMML, ECMA-376 Part 1 §22.1) read with `nodalia_math::omml`.

use nodalia_wordmodel::math::{Math, MathJc, MathProps};
use nodalia_wordmodel::props::Rgb;

use crate::xml::{El, Node};

/// This reader's tree as `nodalia-xml`'s, which `nodalia_math::omml` reads. Both use the canonical
/// prefixes (`m:`, `w:`, `mc:`).
// shortcut: copies the equation's subtree; goes when the reader reads nodalia_xml::El directly.
fn to_craft(e: &El) -> nodalia_xml::El {
    let mut out = nodalia_xml::El { name: e.name.clone(), attrs: e.attrs.clone(), children: Vec::with_capacity(e.kids.len()) };
    for k in &e.kids {
        out.children.push(match k {
            Node::El(c) => nodalia_xml::Node::El(to_craft(c)),
            Node::Text(t) => nodalia_xml::Node::Text(t.clone()),
        });
    }
    out
}

/// An `m:oMath` element as an equation (structure plus its source XML).
pub fn read_omath(e: &El, jc: MathJc) -> Math {
    nodalia_math::omml::read_omath(&to_craft(e), jc)
}

/// The colour every run of `math` shares, taken off the runs (the run around the equation
/// carries it).
pub fn lift_color(math: &mut Math) -> Option<Rgb> {
    nodalia_math::omml::lift_color(math)
}

/// The justification an `m:oMathPara` gives its equations.
pub fn para_jc(para: &El) -> MathJc {
    nodalia_math::omml::para_jc(&to_craft(para))
}

/// `m:mathPr` in the settings part.
pub fn read_math_pr(e: &El) -> MathProps {
    nodalia_math::omml::read_math_pr(&to_craft(e))
}
