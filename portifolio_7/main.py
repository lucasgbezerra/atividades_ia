
import pygame
import numpy as np
from kalman_filter import FiltroDeKalman

RED  = (255, 0, 0)
BLUE = (0,0,255)

def mostraInformacoes(med, pred):
    txtPred = f"Medição: ({med[0]:.1f}, {med[1]:.1f})"
    txtMed = f"Predição: ({pred[0]:.1f}, {pred[1]:.1f})"
    medicao = font.render(txtMed, True, BLUE)
    predicao = font.render(txtPred, True, RED)

    print(txtMed + " Vs " + txtPred)
    
    screen.fill((255, 255, 255))
    screen.blit(medicao, (30, 60))
    screen.blit(predicao, (30, 30))
    pygame.draw.circle(screen, BLUE, (med[0], med[1]), 5)
    pygame.draw.circle(screen, RED, (pred[0], pred[1]), 10)


def movimentoMouse(x, y):
    medicaoAtual = np.array([[np.float32(x)], [np.float32(y)]])
    predicaoAtual = kalman.predicao()

    mx, my = medicaoAtual[0], medicaoAtual[1]
    px, py = predicaoAtual[0], predicaoAtual[1]
    
    mostraInformacoes((float(mx), float(my)), (float(px), float(py)))

    kalman.atualizacao(medicaoAtual)


matrizEstados = np.zeros((4, 1), np.float32)
covarianciaDeEstadoEstimada = np.eye(matrizEstados.shape[0])
matrizTransicao = np.array([[1, 0, 1, 0],[0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
matrizCovarianciaRuido = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], np.float32) * 0.001
medidaEstado = np.zeros((2, 1), np.float32)
matrizEstadoParaMedida = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
matrizCovarianciaMedida = np.array([[1,0],[0,1]], np.float32) * 1

kalman = FiltroDeKalman(X=matrizEstados,
                      P=covarianciaDeEstadoEstimada,
                      A=matrizTransicao,
                      Q=matrizCovarianciaRuido,
                      Z=medidaEstado,
                      H=matrizEstadoParaMedida,
                      R=matrizCovarianciaMedida)

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Tracking do Mouse")
screen.fill((255, 255, 255))
font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mouseX, mouseY = pygame.mouse.get_pos()
    movimentoMouse(mouseX, mouseY)
    
    pygame.display.update()

pygame.quit()
