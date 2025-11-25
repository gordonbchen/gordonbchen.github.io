---
title: "PDEs: Laplace Equation"
layout: post
---


# Laplace PDE:

$$\Delta u = 0 \qquad \left( \Delta u = u_{xx} + u_{yy} \right)$$


# Product Solution:
Assume $u(x, y) = X(x) Y(y)$.

Then

$$\Delta u = X'' Y + X Y'' = 0$$

$$\frac{X''}{X} = -\frac{Y''}{Y} = c$$

$c=0$:

$$Y'' = 0 \implies Y = d_1 y + d_2$$

$$X'' = 0 \implies X = c_1 x + c_2$$

$$u = (d_1 y + d_2) (c_1 x + c_2)$$

$c=\lambda^2, \lambda > 0$

$$Y'' + \lambda^2 Y = 0 \implies Y = d_1 \sin(\lambda y) + d_2 \cos(\lambda y)$$

$$X'' - \lambda^2 X = 0 \implies X = c_1 \sinh(\lambda x) + c_2 \cosh(\lambda x)$$

$$u = \left[ d_1 \sin(\lambda y) + d_2 \cos(\lambda y) \right] \left[ (c_1 \sinh(\lambda x) + c_2 \cosh(\lambda x) \right]$$

$c=-\lambda^2, \lambda > 0$

$$Y'' - \lambda^2 Y = 0 \implies Y = d_1 \sinh(\lambda y) + d_2 \cosh(\lambda y)$$

$$X'' + \lambda^2 X = 0 \implies X = c_1 \sin(\lambda x) + c_2 \cos(\lambda x)$$

$$u = \left[ d_1 \sinh(\lambda y) + d_2 \cosh(\lambda y) \right] \left[ (c_1 \sin(\lambda x) + c_2 \cos(\lambda x) \right]$$


# Dirichlet Boundary Problem on a Rectangle:

### Non-Zero Bottom Edge:
{% include post-img.html file="dp_rect_x0.png" width="60%" %}

Problem:

$$\Delta u = 0$$

$$u(x, 0) = f(x) \qquad u(x, M) = 0$$

$$u(0, y) = 0 \qquad u(L, y) = 0$$

Considering the BC:

$$u(0, y) = u(L, y) = 0 \implies X(0) = X(L) = 0$$

$c = 0$:

$$X = c_1 x + c_2 \implies X = 0$$

$$u = 0, \ \text{trivial solution}$$

$c = \lambda^2$:

$$X = c_1 \sinh(\lambda x) + c_2 \cosh(\lambda x)$$

$$X(0) = c_1 \sinh(0) + c_2 \cosh(0) = c_2 = 0$$

$$X(L) = c_1 \sinh(\lambda L) = 0 \implies c_1 = 0$$

$$X = 0, \ u = 0, \ \text{trivial solution}$$

$c = -\lambda^2$:

$$X = c_1 \sin(\lambda x) + c_2 \cos(\lambda x)$$

$$X(0) = c_1 \sin(0) + c_2 \cos(0) = c_2 = 0$$

$$X(L) = c_1 \sin(\lambda L) = 0 \implies \lambda_n = \frac{n \pi}{L}$$

$$X_n = \sin(\lambda_n x), \lambda_n = \frac{n \pi}{L}$$

$$u_n = \left[ d_1 \sinh(\lambda_n y) + d_2 \cosh(\lambda_n y) \right] \sin(\lambda_n x) \qquad \lambda_n = \frac{n \pi}{L}$$

Considering the BC:

$$u(x, M) = 0 \implies Y(M) = 0$$

$$Y = d_1 \sinh(\lambda_n y) + d_2 \cosh(\lambda_n y)$$

$$Y(M) = d_1 \sinh(\lambda_n M) + d_2 \cosh(\lambda_n M) = 0$$

$$d_1 = -\cosh(\lambda_n M) \qquad d_2 = \sinh(\lambda_n M) = 0$$

$$Y = -\cosh(\lambda_n M) \sinh(\lambda_n y) + \sinh(\lambda_n M) \cosh(\lambda_n y)$$

$$Y = \sinh \left[ \lambda_n (M - y) \right]$$

So:

$$u_n = \sinh \left[ \lambda_n (M - y) \right] \sin(\lambda_n x) \qquad \lambda_n = \frac{n \pi}{L}$$

$$u = \sum_{n=1}^\infty a_n \sinh \left[ \lambda_n (M - y) \right] \sin(\lambda_n x) \qquad \lambda_n = \frac{n \pi}{L}$$


### Non-Zero Top Edge:

$$u(x, 0) = 0 \qquad u(x, L) = g(x)$$

Same BC for $u(0, y) = u(L, y) = 0$, so we still have :

$$u_n = \left[ d_1 \sinh(\lambda_n y) + d_2 \cosh(\lambda_n y) \right] \sin(\lambda_n x) \qquad \lambda_n = \frac{n \pi}{L}$$

Considering the BC:

$$u(x, 0) = 0 \implies Y(0) = 0$$

$$Y = d_1 \sinh(\lambda_n y) + d_2 \cosh(\lambda_n y)$$

$$Y(0) = d_1 \sinh(0) + d_2 \cosh(0) = d_2 = 0$$

$$Y = \sinh(\lambda_n y)$$

So:

$$u_n = \sinh(\lambda_n y) \sin(\lambda_n x) \qquad \lambda_n = \frac{n \pi}{L}$$


### Non-Zero Left and Right Edges:
Just swap x and y.

$u(0, y) = h(y) \qquad y(L, y) = 0$:

$$u_n = \sinh(\gamma_n (L - x)) \sin(\gamma_n y) \qquad \gamma_n = \frac{n \pi}{M}$$

$u(0, y) = 0 \qquad y(L, y) = k(y)$:

$$u_n = \sinh(\gamma_n x) \sin(\gamma_n y) \qquad \gamma_n = \frac{n \pi}{M}$$


### Generalizing:
{% include post-img.html file="dp_rect.png" width="60%" %}

Problem:

$$\Delta u = 0$$

$$u(x, 0) = f(x) \qquad u(x, M) = g(x)$$

$$u(0, y) = h(y) \qquad u(L, y) = k(y)$$

By Linearity:

$$u = u^1 + u^2 + u^3 + u^4$$

Where

$$u^1(x, 0) = f(x) \qquad u^2(x, M) = g(x)$$

$$u^3(0, y) = h(y) \qquad u^4(L, y) = k(y)$$

And

$$u_n^1 = \sinh \left[ \lambda_n (M - y) \right] \sin(\lambda_n x) \qquad \lambda_n = \frac{n \pi}{L}$$

$$u_n^2 = \sinh(\lambda_n y) \sin(\lambda_n x)$$

$$u_n^3 = \sinh(\gamma_n (L - x)) \sin(\gamma_n y) \gamma_n = \frac{n \pi}{M}$$

$$u_n^4 = \sinh(\gamma_n x) \sin(\gamma_n y)$$
