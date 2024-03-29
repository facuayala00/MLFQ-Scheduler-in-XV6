#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fs.h"
#include "kernel/fcntl.h"

#define OPSIZE 16
#define TIMES 32
#define MINTICKS 100

static char path[] = "12iops";
static char data[OPSIZE];

int
main(int argc, char *argv[])
{
  int rfd, wfd;
  int pid = getpid();
  int i;

  path[0] = '0' + (pid / 10);
  path[1] = '0' + (pid % 10);

  memset(data, 'a', sizeof(data));

  int start = uptime();
  int ops = 0;
  for(;;) {
    int end = uptime();
    int elapsed = end - start;
    if (elapsed >= MINTICKS) {
        printf("\t\t\t\t\t%d, %d IOP%dT\n", pid, (int) (ops * MINTICKS / elapsed), MINTICKS);

        start = end;
        ops = 0;
    }

    wfd = open(path, O_CREATE | O_WRONLY);
    rfd = open(path, O_RDONLY);

    for(i = 0; i < TIMES; ++i) {
      write(wfd, data, OPSIZE);
    }
    for(i = 0; i < TIMES; ++i) {
      read(rfd, data, OPSIZE);
    }
    close(wfd);
    close(rfd);
    ops += 2 * TIMES;
  }

  exit(0);
}

