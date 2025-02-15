#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "librcb4/inc/rcb4.h"

#define DEVICE_PATH "/dev/ttyUSB0"

rcb4_connection* conn;
rcb4_comm* comm = NULL;

uint8_t serial_res[256];
int res_bytes;
uint8_t isConnInitialized = 0;
uint8_t isCommInitialized = 0;

typedef enum {
    HEAD_Y = 1,
    BODY_Y,
    L_SHOULDER_P, R_SHOULDER_P,
    L_SHOULDER_R, R_SHOULDER_R,
    L_ELBOW_Y, R_ELBOW_Y,
    L_ELBOW_P, R_ELBOW_P,
    L_HIP_Y, R_HIP_Y,
    L_HIP_R, R_HIP_R,
    L_HIP_P, R_HIP_P,
    L_KNEE_P, R_KNEE_P,
    L_ANKLE_P, R_ANKLE_P,
    L_ANKLE_R, R_ANKLE_R
} SERVO_NAME;


extern int deinit(void) {
    rcb4_command_delete(comm);
    rcb4_deinit(conn);
    isConnInitialized = 0;
    isCommInitialized = 0;
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
    rcb4_command_set_src_ram(comm, 0x0000, 2);
    rcb4_command_set_dst_com(comm);
    res_bytes = rcb4_send_command(conn, comm, serial_res);

    if (res_bytes < 0) {
        printf("Error: reading system configuration\n");
        deinit();
        return -1;
    } else if (res_bytes >= 2) {
        printf("Configretion word = 0x%04X\n", *(uint16_t*)serial_res);
    } else {
        printf("Could not read the configration word correctly\n");
    }

    isConnInitialized = 1;
    printf("Connection established\n");
}

extern int init_command(uint8_t speed) {
    printf("Initializing command...\n");
    if (!isConnInitialized) {
        printf("Connection not initialized\n");
        return -1;
    }
    rcb4_command_recreate(comm, RCB4_COMM_CONST);
    rcb4_command_set_speed(comm, speed);
    printf("Command(CONST) initialized\n");

    isCommInitialized = 1;
    return 0;
}

extern int add_command(SERVO_NAME ics, uint8_t speed, uint16_t pos) {
    if (!isConnInitialized) {
        printf("Connection not initialized\n");
        return -1;
    } else if (!isCommInitialized) {
        printf("Command not initialized\n");
        return -1;
    }
    rcb4_command_set_servo(comm, ics, speed, pos);
    printf("Command added\n");

    return 0;
}

extern int send_command(void) {
    if (!isConnInitialized) {
        printf("Connection not initialized\n");
        return -1;
    } else if (!isCommInitialized) {
        printf("Command not initialized\n");
        return -1;
    }

    return rcb4_send_command(conn, comm, serial_res);
}
