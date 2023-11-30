#include <net-snmp/net-snmp-config.h>
#include <net-snmp/net-snmp-includes.h>
#include <net-snmp/agent/net-snmp-agent-includes.h>

void init_program_snmp()
{
    init_snmp("agente_snmp");
    init_mib();
}

netsnmp_session *create_snmp_session(const char *target, const char *community)
{
    netsnmp_session session, *ss;

    snmp_sess_init(&session);
    session.peername = strdup(target);
    session.community = (unsigned char *)strdup(community);
    session.community_len = strlen(community);
    session.version = SNMP_VERSION_2c; // Set the SNMP version here

    SOCK_STARTUP;

    ss = snmp_open(&session);

    if (!ss)
    {
        snmp_perror("snmp_open");
        snmp_log(LOG_ERR, "Failed to open SNMP session to %s with community %s\n", target, community);
        exit(1);
    }

    return ss;
}

void print_snmp_response(netsnmp_pdu *response)
{
    netsnmp_variable_list *var;

    for (var = response->variables; var; var = var->next_variable)
    {
        print_variable(var->name, var->name_length, var);
    }
}

void get_snmp_info(netsnmp_session *ss, const oid *target_oid)
{
    netsnmp_pdu *pdu;
    netsnmp_pdu *response;

    pdu = snmp_pdu_create(SNMP_MSG_GET);
    snmp_add_null_var(pdu, target_oid, OID_LENGTH(target_oid));

    if (snmp_synch_response(ss, pdu, &response) == STAT_SUCCESS)
    {
        if (response->errstat == SNMP_ERR_NOERROR)
        {
            // Print or process the response
            print_snmp_response(response);
        }
        else
        {
            snmp_perror("SNMP GET");
            snmp_log(LOG_ERR, "Error in SNMP response: %s\n", snmp_errstring(response->errstat));
        }
    }
    else
    {
        snmp_perror("SNMP GET");
        snmp_log(LOG_ERR, "Failed to get SNMP response\n");
    }

    snmp_free_pdu(response);
}

void cleanup_snmp(netsnmp_session *ss)
{
    snmp_close(ss);
    SOCK_CLEANUP;
}

int main()
{
    const char *target = "localhost";
    const char *community = "public";
    const oid target_oid[] = {1, 3, 6, 1, 2, 1, 1, 1, 0}; // Example: System Description

    init_program_snmp();
    netsnmp_session *ss = create_snmp_session(target, community);

    get_snmp_info(ss, target_oid);

    cleanup_snmp(ss);

    return 0;
}
