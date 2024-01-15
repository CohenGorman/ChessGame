import pygame

from data.classes.Piece import Piece

class Pawn(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		img_path = 'data/imgs/' + color[0] + '_pawn.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.square_width - 35, board.square_height - 35))

		self.notation = ' '
		#self.en_passant = False


	def get_possible_moves(self, board):
		output = []
		moves = []
		self.en_passant = False
		self.passant = None

		# move forward
		if self.color == 'white':
			moves.append((0, -1))
			if not self.has_moved:
				moves.append((0, -2))

		elif self.color == 'black':
			moves.append((0, 1))
			if not self.has_moved:
				moves.append((0, 2))

		if board.en_passant == True:
			if board.passant_pos == (self.x + 1, self.y):
				self.en_passant = True
			if board.passant_pos == (self.x - 1, self.y):
				self.en_passant = True

		for move in moves:
			old_pos = (self.x, self.y)
			new_pos = (self.x, self.y + move[1])
			if self.en_passant:
				if self.color == "white":
					self.passant = (board.passant_pos[0], board.passant_pos[1] - 1)
				else:
					self.passant = (board.passant_pos[0], board.passant_pos[1] + 1)
				
				value = board.en_passant_to_check(self.color, old_pos, board.passant_pos)
				if not value:
					output.append(
						board.get_square_from_pos(self.passant)
					)

			if new_pos[1] < 8 and new_pos[1] >= 0:
				output.append(
					board.get_square_from_pos(new_pos)
				)
		

		return output

	def get_moves(self, board):
		output = []
		for square in self.get_possible_moves(board):
			if square.occupying_piece != None:
				break
			else:
				output.append(square)

		if self.color == 'white':
			if self.x + 1 < 8 and self.y - 1 >= 0:
				square = board.get_square_from_pos(
					(self.x + 1, self.y - 1)
				)
				if square.occupying_piece != None:
					if square.occupying_piece.color != self.color:
						output.append(square)
			if self.x - 1 >= 0 and self.y - 1 >= 0:
				square = board.get_square_from_pos(
					(self.x - 1, self.y - 1)
				)
				if square.occupying_piece != None:
					if square.occupying_piece.color != self.color:
						output.append(square)

		elif self.color == 'black':
			if self.x + 1 < 8 and self.y + 1 < 8:
				square = board.get_square_from_pos(
					(self.x + 1, self.y + 1)
				)
				if square.occupying_piece != None:
					if square.occupying_piece.color != self.color:
						output.append(square)
			if self.x - 1 >= 0 and self.y + 1 < 8:
				square = board.get_square_from_pos(
					(self.x - 1, self.y + 1)
				)
				if square.occupying_piece != None:
					if square.occupying_piece.color != self.color:
						output.append(square)

		return output

	def attacking_squares(self, board):
		moves = self.get_moves(board)
		# return the diagonal moves 
		return [i for i in moves if i.x != self.x]

