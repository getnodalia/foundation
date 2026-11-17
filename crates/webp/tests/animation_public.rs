//! Guard the public module wiring: the implementation must be usable by consumers.
#[test]
fn public_animation_api_refuses_empty_movies() {
    let result = nodalia_webp::anim::animation(1, 1, &[], &nodalia_webp::anim::AnimOptions::default());
    assert!(result.is_err());
}
