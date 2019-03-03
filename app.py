import module


def main(game):
    # 게임 실행
    while 1:
        if game.state == 'Running':
            game.event()

            game.input()

            game.create_enemies()

            game.move()

            game.check_collide()

            game.check_state()

            game.draw()

            game.wellfare()

            game.next_process()

        elif game.state == 'Ready':
            game.show_ready_scene()
            game.event()

        elif game.state == 'Pause':
            game.show_pause_scene()
            game.event()

        elif game.state == 'Stop':
            game.show_stop_scene()
            game.event()


if __name__ == '__main__':
    game = module.Game()

    main(game)
