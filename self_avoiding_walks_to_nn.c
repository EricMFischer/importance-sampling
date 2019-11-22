/*
Eric Fischer
UID: 303 759 361
emfischer712@ucla.edu

a) What is the total number K of SAWs for n=10? Plot K against m in a log-log plot and monitor
whether the Sequential Importance Sampling (SIS) process has converged. Try to compare at least
3 different designs for p(r) and see which is most efficient.
b) What is the total number of SAWs that start from (0,0) and end at (n,n)? As we noted,
the truth number is 1.5687x10^24.
c) For each experiment in a) and b), plot the distribution of the lengths N of the SAWs
in a histogram (think: do you need to weight the SAWs in calculating the histogram?) and
visualize (print) the longest SAW found.
*/
/* ---------------------------------------- DESIGN 3 ---------------------------------------- */
/*
a) To estimate the total SAWs, we use Monte Carlo integration.
We design a trial probability g(x) for a SAW, x, that is easier to sample.
We then sample M SAWs from g(x) and estimate total count by omega = 1/M * sum_m(1/g(x_i)).
Thus the problem lies in how to design g(x).
Assume n = 10 and we want to generate M = 10^7 samples.

3 designs for g(x):
Design 1: g_1(x) = product_m(1/k_j), where M = total length of path, k_j = choices for jth move.
At step j, sample uniformly from the k_j choices.
Distribution will resemble a Gaussian because we do not constrain the length of walk.

Design 2: g_2(x) = (1 - eps)^m * product_m(1/k_j).
Introduces early termination probability eps = 0.1, lending shorter but more walks than design 1.
In log-log plot of K SAWs over samples M, sequential importance sampling (SIS) converges slowest.

Design 3:
Adjusts design 1 to favor longer walks.
For any walk longer than 50, generate 5 more children from that branch of the walk, reweighting
each of the children by w_0 = w/5.
Generates over twice as many walks as Design 1 and more than Design 2 as well.
SIS converges FASTEST.

b) Generating 10^6 samples, total SAWs stretching from (0,0) to (n,n) estimated at 1.7403 x 10^24.
*/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

const int M = 1000000;
const int n = 10;
const double eps = 0;
double estimated_SAWs[1000000];
int hist[2][200];
int longest_path_idcs[2][200];
int longest_path = 0;
int gen_walks = 0;

double* get_direction_and_prob(int len_choices, double eps)
{
  // sets probabilities
  double pr[4];
  int i;
  for (i=0; i<=len_choices; i++) {
    pr[i] = (1 - eps) / len_choices;
  }

  // uniform sampling between directions
  int rand_n = rand() % 1000;
  double dir_1_th = 1000 * (eps + pr[0]);
  double dir_2_th = 1000 * (eps + pr[0] + pr[1]);
  double dir_3_th = 1000 * (eps + pr[0] + pr[1] + pr[2]);
  double dir_4_th = 1000 * (eps + pr[0] + pr[1] + pr[2] + pr[3]);

  static double dir_pr[2];
  if (rand_n < 1000 * eps) {
    dir_pr[0] = 0;
    dir_pr[1] = eps;
    return dir_pr;
  } else if (rand_n < dir_1_th) {
    dir_pr[0] = 1;
    dir_pr[1] = pr[0];
    return dir_pr;
  } else if (rand_n < dir_2_th) {
    dir_pr[0] = 2;
    dir_pr[1] = pr[1];
    return dir_pr;
  } else if (rand_n < dir_3_th) {
    dir_pr[0] = 3;
    dir_pr[1] = pr[2];
    return dir_pr;
  } else if (rand_n < dir_4_th) {
    dir_pr[0] = 4;
    dir_pr[1] = pr[3];
    return dir_pr;
  }
  return 0;
}

double generate_child(int grid[n+3][n+3], int x, int y, int n_steps, double g_x, FILE *f_3) {
  double *dir_pr;
  int dir;
  const int dim = n + 3;
  const int last_i = n + 2;

  while (x > 0 && x < last_i && y > 0 && y < last_i) {
    grid[x][y] = 1;
    int i;
    int len_choices = 0;
    int choices[5] = {0};
    int nbrs[4] = {grid[x-1][y], grid[x+1][y], grid[x][y+1], grid[x][y-1]};

    if (nbrs[0] && nbrs[1] && nbrs[2] && nbrs[3]) {
      break;
    }

    for (i=0; i<4; i++) {
      if (!nbrs[i]) {
        len_choices++;
        choices[len_choices] = i + 1;
      }
    }

    dir_pr = get_direction_and_prob(len_choices, eps);
    dir = choices[(int) dir_pr[0]];
    g_x *= dir_pr[1];

    if (dir == 0) {
      break;
    } else if (dir == 1) {
      x -= 1;
    } else if (dir == 2) {
      x += 1;
    } else if (dir == 3) {
      y += 1;
    } else if (dir == 4) {
      y -= 1;
    } else {
      break;
    }

    n_steps++;
    hist[0][n_steps] = x;
    hist[1][n_steps] = y;
  }

  int end = n + 1;
  if (x == end && y == end) {
    g_x *= -7; // for 7 children
    if (n_steps > longest_path) {
      longest_path = n_steps;
      memcpy(longest_path_idcs, hist, sizeof(hist));
    }
    fprintf(f_3, "%d\n", n_steps);
  } else {
    g_x *= 7;
  }

  return g_x;
}

double generate_SAWs(int M, int n, FILE *f_1, FILE *f_2, FILE *f_3)
{
  srand(0);

  double *dir_pr;
  const int dim = n + 3;
  const int last_i = n + 2;
  int grid[dim][dim];
  int gen_walks = 0;
  double wt_sum = 0;
  int i, j;
  int tries;

  while (gen_walks < M) {
    tries = 0;
    while (1) {
      for (i=0; i<dim; i++) {
        for (j=0; j<dim; j++) {
          if (i==0 || j==0 || i==last_i || j==last_i) {
            grid[i][j] = 1;
          } else {
            grid[i][j] = 0;
          }
        }
      }

      int dir;
      int x = 1, y = 1;
      int n_steps = 0;
      double g_x = 1;
      memset(hist, 100, sizeof(hist));
      hist[0][0] = x;
      hist[1][0] = y;

      const int checkpoint = 90;
      while (x > 0 && x < last_i && y > 0 && y < last_i) {
        grid[x][y] = 1;
        int len_choices = 0;
        int choices[5] = {0};
        int nbrs[4] = {grid[x-1][y], grid[x+1][y], grid[x][y+1], grid[x][y-1]};

        if (nbrs[0] && nbrs[1] && nbrs[2] && nbrs[3]) {
          break;
        }

        for (i=0; i<4; i++) {
          if (!nbrs[i]) {
            len_choices++;
            choices[len_choices] = i + 1;
          }
        }

        dir_pr = get_direction_and_prob(len_choices, eps);
        dir = choices[(int) dir_pr[0]];

        if (dir == 0) {
          break;
        } else if (dir == 1) {
          x -= 1;
        } else if (dir == 2) {
          x += 1;
        } else if (dir == 3) {
          y += 1;
        } else if (dir == 4) {
          y -= 1;
        } else {
          break;
        }

        n_steps++;
        hist[0][n_steps] = x;
        hist[1][n_steps] = y;

        if (n_steps > checkpoint) {
          int temp[dim][dim];
          int child = 0;

          while (child < 7) {
            double g_x_temp;
            memcpy(temp, grid, sizeof(grid));
            g_x_temp = generate_child(temp, x, y, n_steps, g_x, f_3);
            tries++;
            if (g_x_temp <= 0) {
              g_x = g_x_temp;
              break;
            }
            child++;
          }
          break;
        } else {
          g_x *= dir_pr[1];
        }
      }

      if (n_steps > checkpoint) {
        if (g_x <= 0) {
          wt_sum = wt_sum - (1 / g_x / tries);
          gen_walks++;
          estimated_SAWs[gen_walks] = wt_sum / gen_walks;
          fprintf(f_1, "%e %e\n", estimated_SAWs[gen_walks], -1 / g_x / tries);
          break;
        }
      } else {
        tries++;
        int end = n + 1;
        if (x == end && y == end) {
          wt_sum = wt_sum + 1 / g_x / tries;
          gen_walks++;
          estimated_SAWs[gen_walks] = wt_sum / gen_walks;
          fprintf(f_1, "%e %e\n", estimated_SAWs[gen_walks], 1 / g_x / tries);
          fprintf(f_3, "%d\n", n_steps);
          break;
        }
      }
    }
  }

  for (i=0; i<longest_path+1; i++) {
    fprintf(f_2, "%d %d\n", longest_path_idcs[0][i], longest_path_idcs[1][i]);
  }

  return wt_sum / M;
}



int main(void)
{
  FILE *f_1 = fopen("design_4_saws.txt", "w");
  FILE *f_2 = fopen("design_4_longest_path.txt", "w");
  FILE *f_3 = fopen("design_4_steps.txt", "w");
  printf("SAWs: %e \n", generate_SAWs(M, n, f_1, f_2, f_3));
  fclose(f_1);
  fclose(f_2);
  fclose(f_3);
  getchar();
  return 0;
}
