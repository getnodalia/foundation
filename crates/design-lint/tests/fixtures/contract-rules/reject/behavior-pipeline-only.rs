use nodalia_behavior::Gesture;
use nodalia_behavior::TypingRun;
use nodalia_behavior::press::PressMachine;
use nodalia_behavior::press::PassInput as Input;
use nodalia_behavior::press;
use crate::runtime::focus::push_scope;

fn open(ctx: &Context, id: Id, policy: FocusPolicy) {
    crate::runtime::focus::push_scope(ctx, id, policy, None);
    crate::runtime::focus::pop_scope(ctx);
}

fn run(gesture: nodalia_behavior::Gesture<f32>, step: PressStep<u32>) {}

fn count(previous: Option<(Pos2, f64, u32)>) -> u32 {
    count_clicks(previous, pos, time, slop)
}
