import pygame
import librosa as lbr
from random import choice
import cv2  # pip install opencv-python
import numpy as np


class BeatsGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        # Game settings
        self.width = 800
        self.height = 600
        self.fall_speed = 5  # Pixels per animation frame
        self.endline_y = self.height - 80  # Y position for the endline
        self.tolerance = 50  # Tolerance in pixels before and after the endline

        # Colors
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)

        # Load main menu background video
        self.menu_video_path = "mainbg.mov"
        self.menu_video = cv2.VideoCapture(self.menu_video_path)
        self.menu_frame_rate = self.menu_video.get(cv2.CAP_PROP_FPS)
        self.menu_frame_time = int(1000 / self.menu_frame_rate)

        # Initialize display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("YAMI")

        # Allow player to select the video
        self.video_options = ["bg2.mov", "bg3.mp4", "bg4.mov"]
        self.video_path = self.select_video()
        self.video = cv2.VideoCapture(self.video_path)
        self.frame_rate = self.video.get(cv2.CAP_PROP_FPS)
        self.frame_time = int(1000 / self.frame_rate)

        # initialize scoring system
        self.beats = []
        self.start_time = pygame.time.get_ticks()
        self.score = 0
        self.game_over = False

        # Load beat image
        self.beat_image = pygame.image.load("music6.png").convert_alpha()
        self.beat_image = pygame.transform.scale(self.beat_image, (70, 70))

        # Load audio
        self.audio_path = "believer.mp3"  # connect this with music player
        self.y, self.sr = lbr.load(self.audio_path)
        self.harmonic, self.percussive = lbr.effects.hpss(self.y)

        # Increase hop length or adjust lag for onset sensitivity
        onset_env = lbr.onset.onset_strength(
            y=self.harmonic, sr=self.sr, hop_length=512, lag=1
        )

        # Detect beats and smooth them
        self.tempo, _ = lbr.beat.beat_track(
            onset_envelope=onset_env, sr=self.sr
        )
        self.beat_frames, self.beat_indices = lbr.beat.beat_track(
            onset_envelope=onset_env, sr=self.sr
        )
        self.beat_time = lbr.frames_to_time(self.beat_indices, sr=self.sr)

        # Apply smoothing to remove irregular beats
        self.beat_time = self.filter_major_beats(self.beat_time)

        # Additional smoothing using simple moving average
        self.beat_time = self.smooth_beats(self.beat_time)

        duration = len(self.y) / self.sr
        print(duration)

        # print("Filtered beats:", self.beat_time)

        # Initialize Pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.play(0)

        # Display main menu
        self.show_main_menu()

        self.beats = []  # To keep track of beats
        self.start_time = pygame.time.get_ticks()
        self.score = 0  # Initialize score

        # Run the game
        self.run_game()

    def load_background_video(self, video_path):
        # Load and return the video capture object and frame rate.
        video = cv2.VideoCapture(video_path)
        frame_rate = video.get(cv2.CAP_PROP_FPS)
        frame_time = int(1000 / frame_rate)
        return video, frame_rate, frame_time

    def draw_menu_background(self):
        """Draw the menu background from video."""
        ret, frame = self.menu_video.read()
        if ret:
            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.transpose(frame, (1, 0, 2))
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
        else:
            self.menu_video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def show_main_menu(self):
        # Display the main menu with video background.
        self.menu_video, self.menu_frame_rate, self.menu_frame_time = (
            self.load_background_video(self.menu_video_path)
        )

        running = True
        while running:
            self.draw_menu_background()
            font = pygame.font.Font(None, 36)
            text = font.render(
                "Select a Background Video (1-3):", True, self.white
            )
            self.screen.blit(text, (200, 100))

            for i, option in enumerate(self.video_options, start=1):
                option_text = font.render(f"{i}. {option}", True, self.white)
                button_rect = pygame.Rect(200, 150 + 50 * i, 200, 40)
                pygame.draw.rect(self.screen, self.red, button_rect, 2)
                self.screen.blit(
                    option_text, (button_rect.x + 10, button_rect.y + 10)
                )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, option in enumerate(self.video_options, start=1):
                        button_rect = pygame.Rect(200, 150 + 50 * i, 200, 40)
                        if button_rect.collidepoint(event.pos):
                            self.video_path = option
                            self.video, self.frame_rate, self.frame_time = (
                                self.load_background_video(self.video_path)
                            )
                            self.video.set(
                                cv2.CAP_PROP_POS_FRAMES, 0
                            )  # Restart the video
                            self.video_options = []  # End video selection menu
                            self.run_game()  # Start the game

    def select_video(self):
        # Display a menu for the user to select a video.
        running = True
        while running:
            self.screen.fill(self.black)
            font = pygame.font.Font(None, 36)
            text = font.render(
                "Select a Background Video (1-3):", True, self.white
            )
            self.screen.blit(text, (200, 100))

            for i, option in enumerate(self.video_options, start=1):
                option_text = font.render(f"{i}. {option}", True, self.white)
                self.screen.blit(option_text, (200, 150 + 50 * i))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return self.video_options[0]
                    elif event.key == pygame.K_2:
                        return self.video_options[1]
                    elif event.key == pygame.K_3:
                        return self.video_options[2]

    def filter_major_beats(self, beat_times):
        if len(beat_times) < 2:
            return beat_times  # Not enough beats to filter

        # Calculate the average beat interval
        intervals = [
            beat_times[i + 1] - beat_times[i]
            for i in range(len(beat_times) - 1)
        ]
        avg_interval = sum(intervals) / len(intervals)

        # Filter beats that are close to the average interval
        filtered_beats = [beat_times[0]]  # Start with the first beat
        for i in range(1, len(beat_times)):
            if (
                abs(beat_times[i] - filtered_beats[-1] - avg_interval)
                < avg_interval * 0.5
            ):
                filtered_beats.append(beat_times[i])

        return filtered_beats

    def smooth_beats(self, beat_times):
        smoothed_beats = []
        window_size = 3  # Adjust the window size for more smoothing
        for i in range(len(beat_times) - window_size):
            avg_time = sum(beat_times[i : i + window_size]) / window_size
            smoothed_beats.append(avg_time)
        return smoothed_beats

    def create_beat(self):
        column_x = choice([100, 350, 600])  # Randomly select a column
        beat_rect = pygame.Rect(column_x, 0, 50, 20)
        beat_data = {"rect": beat_rect}
        self.beats.append(beat_data)
        # print(f"Beat created at column: {column_x}")

    def animate_beats(self):
        for beat in self.beats:
            beat["rect"].y += self.fall_speed  # Move the beat down

            # Remove the beat if it goes out of bounds
            if beat["rect"].y > self.height:
                self.beats.remove(beat)

    def draw_beats(self):
        for beat in self.beats:
            self.screen.blit(self.beat_image, beat["rect"].topleft)

    def draw_endline(self):
        pygame.draw.line(
            self.screen,
            self.green,
            (0, self.endline_y),
            (self.width, self.endline_y),
            2,
        )

    def draw_score(self):
        font = pygame.font.Font(None, 36)  # Use default font and size 36
        score_text = font.render(f"Score: {self.score}", True, self.white)
        self.screen.blit(
            score_text, (10, 10)
        )  # Draw score in the top-left corner

    def draw_background(self):
        # Draw the selected video as background
        ret, frame = self.video.read()
        if ret:
            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.transpose(frame, (1, 0, 2))
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
        else:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def draw_final_score(self):
        font = pygame.font.Font(None, 72)
        score_text = font.render(
            f"Final Score: {self.score}", True, self.white
        )
        self.screen.blit(
            score_text,
            (self.width // 2 - score_text.get_width() // 2, self.height // 3),
        )

    def run_game(self):
        """Run the main game loop."""
        running = True
        clock = pygame.time.Clock()
        beat_index = 0
        start_time = pygame.time.get_ticks() / 1000  # Track game start time

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.restart_button.collidepoint(event.pos):
                            self.__init__()  # Restart game
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_a, pygame.K_s, pygame.K_d]:
                        self.handle_key(event.key)

            current_time = (
                pygame.time.get_ticks() / 1000
            ) - start_time  # Adjust timing

            if not self.game_over:
                # Check if we need to create a new beat
                if (
                    beat_index < len(self.beat_time)
                    and current_time >= self.beat_time[beat_index]
                ):
                    self.create_beat()
                    beat_index += 1

                self.draw_background()
                self.animate_beats()
                self.draw_beats()
                self.draw_endline()
                self.check_collisions()
                self.draw_score()
                pygame.display.flip()

                # Check if the game is over (i.e., no more beats are present)
                if beat_index >= len(self.beat_time) and not self.beats:
                    self.game_over = True
                    pygame.mixer.music.stop()

            # If the game is over, show final score and restart button
            if self.game_over:
                self.restart_button = self.draw_final_score()
                pygame.display.flip()

            clock.tick(60)

        pygame.quit()
        self.video.release()

    def handle_key(self, key):
        columns = {pygame.K_a: 100, pygame.K_s: 350, pygame.K_d: 600}
        if key in columns:
            hit = False
            for beat in self.beats:
                if (
                    abs(beat["rect"].y - self.endline_y) < self.tolerance
                    and beat["rect"].x == columns[key]
                ):
                    self.score += 10
                    self.beats.remove(beat)
                    hit = True
                    break
            if not hit:
                self.score -= 5

    # To check collisions
    def check_collisions(self):
        for beat in self.beats:
            if beat["rect"].y > self.endline_y + self.tolerance:
                self.game_over = True
                pygame.mixer.music.stop()
                self.beats.clear()


if __name__ == "__main__":
    BeatsGame()
