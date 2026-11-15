import os
import pygame
from room_base import Room_Base


class PasslockControl:
    ANSWER = "そつぎょうしき"

    def __init__(self, font):
        self.font = font
        self.passcode = ""
        self.unlocked = False
        self.message = ""

        self.clear_rect = pygame.Rect(570, 561, 147, 43)
        self.confirm_rect = pygame.Rect(733, 561, 159, 43)
        self.keys = []

        normal_rows = [
            "わらやまはなたさかあ",
            " り みひにちしきい",
            "をるゆむふぬつすくう",
            " れ めへねてせけえ",
            "んろよもほのとそこお",
        ]

        for row_index, row in enumerate(normal_rows):
            for column_index, character in enumerate(row):
                if character == " ":
                    continue

                rect = pygame.Rect(
                    123 + column_index * 78,
                    round(211.53 + row_index * 36.48),
                    67,
                    30,
                )
                self.keys.append((rect, character))

        extra_rows = [
            "がぎぐげござじずぜぞだぢ",
            "づでどばびぶべぼぱぴぷぺ",
            "ぽゔぁぃぅぇぉゃゅょっゎ",
        ]

        for row_index, row in enumerate(extra_rows):
            for column_index, character in enumerate(row):
                rect = pygame.Rect(
                    123 + column_index * 65,
                    426 + row_index * 41,
                    54,
                    34,
                )
                self.keys.append((rect, character))

    def onclick(self, x, y):
        if self.clear_rect.collidepoint(x, y):
            self.passcode = ""
            self.message = ""
            return

        if self.confirm_rect.collidepoint(x, y):
            self.unlock()
            return

        for rect, character in self.keys:
            if rect.collidepoint(x, y):
                candidate = self.passcode + character

                if self.font.size(candidate)[0] <= 720:
                    self.passcode = candidate
                    self.message = ""
                return

    def unlock(self):
        if self.passcode == self.ANSWER:
            self.unlocked = True
            self.message = ""
        else:
            self.message = "ちがうようだ。もう一度入力しよう"

    def disp_passcode(self, canvas):
        text = self.font.render(
            self.passcode, True, (73, 61, 51)
        )
        canvas.blit(text, (145, 145))


class Vent(Room_Base):
    IMAGE_SIZE = (1015, 676)

    def __init__(self, screen, lock_flag):
        super().__init__(screen, lock_flag)

        self.panel_visible = False
        self.hint_revealed = False
        self.hint_hover = False
        self.escaped = False

        image_dir = os.path.join(
            os.path.dirname(__file__), "res", "vent", "vent"
        )

        self.img_room = self.load_image(
            image_dir, "vent_lock.png"
        )
        self.img_hint = self.load_image(
            image_dir, "vent_hinnto_matched.png"
        )
        self.img_panel = self.load_image(
            image_dir, "panel.png"
        )
        self.img_open = self.load_image(
            image_dir, "vent_open.png"
        )

        self.hint_rect = pygame.Rect(128, 499, 85, 85)
        self.panel_rect = pygame.Rect(430, 453, 145, 112)
        self.exit_rect = pygame.Rect(323, 297, 177, 324)
        self.back_rect = pygame.Rect(123, 561, 135, 43)

        self.img_highlight = pygame.Surface(
            self.hint_rect.size, pygame.SRCALPHA
        )
        self.img_highlight.fill((255, 255, 0, 50))

        font_path = pygame.font.match_font(
            "meiryo,yugothic,msgothic,hiraginosans,"
            "notosanscjkjp,notosanscjk"
        )
        self.font = pygame.font.Font(font_path, 30)
        self.small_font = pygame.font.Font(font_path, 20)
        self.large_font = pygame.font.Font(font_path, 52)

        self.passlock = PasslockControl(self.font)
        self.canvas = pygame.Surface(self.IMAGE_SIZE)

    def load_image(self, directory, filename):
        image = pygame.image.load(
            os.path.join(directory, filename)
        ).convert_alpha()

        return pygame.transform.smoothscale(
            image, self.IMAGE_SIZE
        )

    def image_position(self, x, y):
        width, height = self.screen.get_size()

        return (
            x * self.IMAGE_SIZE[0] / width,
            y * self.IMAGE_SIZE[1] / height,
        )

    def pos_event(self, x, y):
        position = self.image_position(x, y)

        self.hint_hover = (
            not self.panel_visible
            and not self.passlock.unlocked
            and not self.hint_revealed
            and not self.escaped
            and self.hint_rect.collidepoint(position)
        )

    def click_event(self, x, y):
        position = self.image_position(x, y)

        if self.escaped:
            return

        if self.panel_visible:
            if self.back_rect.collidepoint(position):
                self.panel_visible = False
                return

            self.passlock.onclick(*position)

            if self.passlock.unlocked:
                self.panel_visible = False
            return

        if self.passlock.unlocked:
            if self.exit_rect.collidepoint(position):
                self.escaped = True
            return

        if self.hint_rect.collidepoint(position):
            self.hint_revealed = True
            self.hint_hover = False

        elif self.panel_rect.collidepoint(position):
            self.panel_visible = True
            self.hint_hover = False
            self.passlock.message = ""

    def do(self):
        pass

    def draw(self):
        canvas = self.canvas

        if self.passlock.unlocked:
            canvas.blit(self.img_open, (0, 0))
        elif self.hint_revealed:
            canvas.blit(self.img_hint, (0, 0))
        else:
            canvas.blit(self.img_room, (0, 0))

        if self.hint_hover:
            canvas.blit(
                self.img_highlight, self.hint_rect.topleft
            )

        if self.panel_visible:
            canvas.blit(self.img_panel, (0, 0))
            self.passlock.disp_passcode(canvas)

            pygame.draw.rect(
                canvas,
                (230, 215, 200),
                self.back_rect,
                border_radius=6,
            )
            pygame.draw.rect(
                canvas,
                (153, 133, 117),
                self.back_rect,
                width=1,
                border_radius=6,
            )

            back_text = self.small_font.render(
                "戻る", True, (73, 61, 51)
            )
            canvas.blit(
                back_text,
                back_text.get_rect(
                    center=self.back_rect.center
                ),
            )

            message = self.small_font.render(
                self.passlock.message,
                True,
                (160, 65, 55),
            )
            canvas.blit(message, (123, 615))

        if self.escaped:
            shade = pygame.Surface(
                self.IMAGE_SIZE, pygame.SRCALPHA
            )
            shade.fill((0, 0, 0, 165))
            canvas.blit(shade, (0, 0))

            text = self.large_font.render(
                "脱出成功！", True, (255, 245, 220)
            )
            canvas.blit(
                text,
                text.get_rect(center=(507, 338)),
            )

        resized = pygame.transform.smoothscale(
            canvas, self.screen.get_size()
        )
        self.screen.blit(resized, (0, 0))
