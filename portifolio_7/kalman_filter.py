import numpy as np

class FiltroDeKalman:
    def __init__(self, A, H, Q, Z, R, P, X, M = np.array([0]), B = np.array([0])):
        self.A = A
        self.H = H
        self.Q = Q
        self.Z = Z
        self.R = R
        self.P = P
        self.X = X
        self.M = M
        self.B = B
        
    def predicao(self):
        self.X = self.A @ self.X + self.B @ self.M
        self.P = self.A @ self.P @ self.A.T + self.Q
        
        return self.X

    def atualizacao(self, Z):
        K = self.P @ self.H.T @ np.linalg.inv(self.H @ self.P @ self.H.T + self.R)
        self.X += K @ (Z - self.H @ self.X)
        self.P = self.P - K @ self.H @ self.P

        return self.X