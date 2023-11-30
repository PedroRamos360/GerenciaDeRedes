#include <net-snmp/net-snmp-config.h>
#include <net-snmp/net-snmp-includes.h>

int main()
{
    init_snmp("simple_agent");

    netsnmp_session session, *ss;
    snmp_sess_init(&session);

    session.version = SNMP_VERSION_2c;
    session.community = (u_char *)"public";
    session.community_len = strlen((const char *)session.community);
    session.peername = "udp:127.0.0.1:161";

    SOCK_STARTUP;
    ss = snmp_open(&session);

    if (!ss)
    {
        snmp_perror("snmp_open");
        snmp_log(LOG_ERR, "Failed to open SNMP session.\n");
        exit(1);
    }

    snmp_log(LOG_INFO, "SNMP agent initialized successfully. Listening for GET requests...\n");

    // Run the SNMP agent indefinitely
    while (1)
    {
        // netsnmp_pdu *pdu;
        fd_set *readfds;

        // Initialize the read file descriptor set
        FD_ZERO(readfds);

        // Block until a request is received
        snmp_sess_read(NULL, readfds);

        printf("Received request");

        // pdu = NULL;

        // switch (pdu->command)
        // {
        // case SNMP_MSG_GET:
        //     printf("Received GET request\n");
        //     break;
        // case SNMP_MSG_GETNEXT:
        //     printf("Received GETNEXT request\n");
        //     break;
        // case SNMP_MSG_SET:
        //     printf("Received SET request\n");
        //     break;
        // case SNMP_MSG_TRAP:
        //     printf("Received TRAP request\n");
        //     break;
        // default:
        //     printf("Unknown request type\n");
        //     break;
        // }
    }

    snmp_close(ss);
    SOCK_CLEANUP;
    return 0;
}
