#!/usr/bin/env python3
"""Minimax with alpha-beta pruning for game trees."""
import sys

def minimax(node,depth,maximizing,alpha=float('-inf'),beta=float('inf'),eval_fn=None,children_fn=None):
    if depth==0 or not children_fn(node):return eval_fn(node),node
    if maximizing:
        best_val=float('-inf');best_move=None
        for child in children_fn(node):
            val,_=minimax(child,depth-1,False,alpha,beta,eval_fn,children_fn)
            if val>best_val:best_val=val;best_move=child
            alpha=max(alpha,val)
            if beta<=alpha:break
        return best_val,best_move
    else:
        best_val=float('inf');best_move=None
        for child in children_fn(node):
            val,_=minimax(child,depth-1,True,alpha,beta,eval_fn,children_fn)
            if val<best_val:best_val=val;best_move=child
            beta=min(beta,val)
            if beta<=alpha:break
        return best_val,best_move

# Tic-tac-toe
def ttt_winner(board):
    lines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in lines:
        if board[a]==board[b]==board[c]!='.':return board[a]
    return None

def ttt_children(state):
    board,player=state;moves=[]
    if ttt_winner(board):return moves
    for i in range(9):
        if board[i]=='.':
            b=list(board);b[i]=player
            moves.append((tuple(b),'O' if player=='X' else 'X'))
    return moves

def ttt_eval(state):
    w=ttt_winner(state[0])
    if w=='X':return 10
    if w=='O':return-10
    return 0

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        # X should win or draw with perfect play
        board=tuple('.'*9)
        val,move=minimax((board,'X'),9,True,eval_fn=ttt_eval,children_fn=ttt_children)
        assert val>=0  # X can at least draw
        # X about to win
        board2=tuple('XX.OO....')
        val2,_=minimax((board2,'X'),9,True,eval_fn=ttt_eval,children_fn=ttt_children)
        assert val2==10  # X wins
        # Alpha-beta should prune (just verify it works)
        board3=tuple('.'*9)
        val3,_=minimax((board3,'X'),9,True,eval_fn=ttt_eval,children_fn=ttt_children)
        assert val3==0  # perfect play = draw
        print("All tests passed!")
    else:
        board=tuple('.'*9)
        val,move=minimax((board,'X'),9,True,eval_fn=ttt_eval,children_fn=ttt_children)
        print(f"Tic-tac-toe value for X: {val}")
if __name__=="__main__":main()
