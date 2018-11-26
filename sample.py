import ai
import snake


def play_easy():
    game = snake.Game(8, 8)
    game.play_new_game(12)


def play_normal():
    game = snake.Game(12, 12)
    game.play_new_game(8)


def play_hard():
    game = snake.Game(16, 16)
    game.play_new_game(4)


def train():
    state_size = 8
    action_size = 4
    episodes = 500
    steps = 600
    game = snake.Game(12, 12)
    model = ai.Model(state_size, action_size)

    for e in range(episodes):
        game.reset()
        tot_reward = 0
        for step in range(steps):
            state = game.state()
            previous_score = game.score
            action = model.act(state)
            alive = game.move(action)
            next_state = None
            reward = game.score - previous_score
            tot_reward += reward
            if alive:
                next_state = game.state()
            else:
                reward -= 1
            model.remember((state, action, reward, next_state))
            model.replay()
        print('Episode {} : score {}'.format(e + 1, game.score))

        if e % 50 == 49:
            tot_score = 0
            for i in range(50):
                game.reset()
                step = 0
                while step < steps:
                    if not game.move(model.act_best(game.state())):
                        break
                    step += 1
                tot_score += game.score
            print(tot_score / 50)

    game.play_new_game(5, model.act_best)


train()
