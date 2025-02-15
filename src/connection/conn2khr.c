#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "librcb4/inc/rcb4.h"

#define DEVICE_PATH "/dev/ttyUSB0"

rcb4_connection* conn;
rcb4_comm* comm = NULL;
rcb4_comm* comm_const = NULL;
enum e_rcb4_command_types current_comm;

uint8_t serial_res[256];
int res_bytes;


extern int deinit(void) {
    rcb4_command_delete(comm);
    rcb4_command_delete(comm_const);
    rcb4_deinit(conn);
    printf("Connection closed\n");

    return 0;
}

extern int init(void) {
    printf("Initializing connection...\n");
    conn = rcb4_init(DEVICE_PATH);
    if (!conn) {
        printf("Connection failed\n");
        return -1;
    }
    printf("Ping: %d\n", rcb4_command_ping(conn));

    printf("Reading system configuration...\n");
    comm = rcb4_command_create(RCB4_COMM_MOV);
    current_comm = RCB4_COMM_MOV;
    rcb4_command_set_src_ram(comm, 0x0000, 2);
    rcb4_command_set_dst_com(comm);
    res_bytes = rcb4_send_command(conn, comm, serial_res);
}