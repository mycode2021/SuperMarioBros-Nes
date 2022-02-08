from torch.nn import functional as F
import argparse, os, time, torch, utils
os.environ["OMP_NUM_THREADS"] = "1"


def get_args():
    args = argparse.ArgumentParser(
        '''Directions: Toolkit for SuperMarioBros-Nes environment.''')
    args.add_argument("--game", type=str, default="SuperMarioBros-Nes")
    args.add_argument("--state", type=str, default="Level2-1")
    args.add_argument("--action_type", type=str, default="simple")
    args.add_argument("--records_path", type=str, default="records")
    args.add_argument("--loading_path", type=str, default="models")
    args.add_argument("--from_model", type=str, default="Level2-1")
    return args.parse_args()

def run_test(opt):
    torch.manual_seed(123)
    memory = "%s/%s"%(opt.loading_path, opt.from_model)
    assert os.path.isfile(memory), "The trained model does not exist."
    xscroll = 0

    try:
        env, num_inputs, num_actions = utils.create_runtime_env(
            opt.game, opt.state, opt.action_type, opt.records_path)
        model = utils.PPO(num_inputs, num_actions)
        model.eval()
        model.load_state_dict(torch.load(memory, map_location=torch.device("cpu")))
        state = torch.from_numpy(env.reset())

        while True:
            logits, value = model(state)
            policy = F.softmax(logits, dim=1)
            action = torch.argmax(policy).item()
            state, reward, done, info = env.step(action)
            xscroll = max(xscroll, info["xscrollHi"]*256+info["xscrollLo"])
            env.render()
            time.sleep(0.03)
            if done:
                print("Level %s Xscroll %d Finish %s."%(opt.state, xscroll, info["finish"]))
                break
            state = torch.from_numpy(state)
    finally:
        env.close()


if __name__ == "__main__":
    run_test(get_args())
