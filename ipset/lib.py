from cffi import FFI

cdef = """
/* nfproto.h */
/*
 * The constants to select, same as in linux/netfilter.h.
 * Like nf_inet_addr.h, this is just here so that we need not to rely on
 * the presence of a recent-enough netfilter.h.
 */
enum {
        NFPROTO_UNSPEC =  0,
        NFPROTO_IPV4   =  2,
        NFPROTO_ARP    =  3,
        NFPROTO_BRIDGE =  7,
        NFPROTO_IPV6   = 10,
        NFPROTO_DECNET = 12,
        NFPROTO_NUMPROTO,
};


/* linux_ip_set.h */
/* Message types and commands */
enum ipset_cmd {
        IPSET_CMD_NONE,
        IPSET_CMD_PROTOCOL,     /* 1: Return protocol version */
        IPSET_CMD_CREATE,       /* 2: Create a new (empty) set */
        IPSET_CMD_DESTROY,      /* 3: Destroy a (empty) set */
        IPSET_CMD_FLUSH,        /* 4: Remove all elements from a set */
        IPSET_CMD_RENAME,       /* 5: Rename a set */
        IPSET_CMD_SWAP,         /* 6: Swap two sets */
        IPSET_CMD_LIST,         /* 7: List sets */
        IPSET_CMD_SAVE,         /* 8: Save sets */
        IPSET_CMD_ADD,          /* 9: Add an element to a set */
        IPSET_CMD_DEL,          /* 10: Delete an element from a set */
        IPSET_CMD_TEST,         /* 11: Test an element in a set */
        IPSET_CMD_HEADER,       /* 12: Get set header data only */
        IPSET_CMD_TYPE,         /* 13: Get set type */
        IPSET_MSG_MAX,          /* Netlink message commands */

        /* Commands in userspace: */
        IPSET_CMD_RESTORE = IPSET_MSG_MAX, /* 14: Enter restore mode */
        IPSET_CMD_HELP,         /* 15: Get help */
        IPSET_CMD_VERSION,      /* 16: Get program version */
        IPSET_CMD_QUIT,         /* 17: Quit from interactive mode */

        IPSET_CMD_MAX,

        IPSET_CMD_COMMIT = IPSET_CMD_MAX, /* 18: Commit buffered commands */
};


/* session.h */
struct ipset_session;
struct ipset_data;
struct ipset_handle;

extern struct ipset_data *
        ipset_session_data(const struct ipset_session *session);
extern struct ipset_handle *
        ipset_session_handle(const struct ipset_session *session);
extern const struct ipset_type *
        ipset_saved_type(const struct ipset_session *session);
extern void ipset_session_lineno(struct ipset_session *session,
                                 uint32_t lineno);

enum ipset_err_type {
        IPSET_ERROR,
        IPSET_WARNING,
};

extern int ipset_session_report(struct ipset_session *session,
                                enum ipset_err_type type,
                                const char *fmt, ...);

extern void ipset_session_report_reset(struct ipset_session *session);
extern const char *ipset_session_error(const struct ipset_session *session);
extern const char *ipset_session_warning(const struct ipset_session *session);

/* Environment option flags */
enum ipset_envopt {
        IPSET_ENV_SORTED        = 1,
        IPSET_ENV_QUIET         = 2,
        IPSET_ENV_RESOLVE       = 4,
        IPSET_ENV_EXIST         = 8,
        IPSET_ENV_LIST_SETNAME  = 16,
        IPSET_ENV_LIST_HEADER   = 32,
};

extern int ipset_envopt_parse(struct ipset_session *session,
                              int env, const char *str);
extern bool ipset_envopt_test(struct ipset_session *session,
                              enum ipset_envopt env);

enum ipset_output_mode {
        IPSET_LIST_NONE,
        IPSET_LIST_PLAIN,
        IPSET_LIST_SAVE,
        IPSET_LIST_XML,
};

extern int ipset_session_output(struct ipset_session *session,
                                enum ipset_output_mode mode);

extern int ipset_commit(struct ipset_session *session);
extern int ipset_cmd(struct ipset_session *session, enum ipset_cmd cmd,
                     uint32_t lineno);

typedef int (*ipset_outfn)(const char *fmt, ...);

extern int ipset_session_outfn(struct ipset_session *session,
                               ipset_outfn outfn);
extern struct ipset_session *ipset_session_init(ipset_outfn outfn);
extern int ipset_session_fini(struct ipset_session *session);


extern void ipset_load_types(void);
extern const struct ipset_type *
        ipset_type_get(struct ipset_session *session, enum ipset_cmd cmd);
extern const struct ipset_type *
        ipset_type_check(struct ipset_session *session);


/* data.h */
/* Data options */
enum ipset_opt {
        IPSET_OPT_NONE = 0,
        /* Common ones */
        IPSET_SETNAME,
        IPSET_OPT_TYPENAME,
        IPSET_OPT_FAMILY,
        /* CADT options */
        IPSET_OPT_IP,
        IPSET_OPT_IP_FROM = IPSET_OPT_IP,
        IPSET_OPT_IP_TO,
        IPSET_OPT_CIDR,
        IPSET_OPT_PORT,
        IPSET_OPT_PORT_FROM = IPSET_OPT_PORT,
        IPSET_OPT_PORT_TO,
        IPSET_OPT_TIMEOUT,
        /* Create-specific options */
        IPSET_OPT_GC,
        IPSET_OPT_HASHSIZE,
        IPSET_OPT_MAXELEM,
        IPSET_OPT_NETMASK,
        IPSET_OPT_PROBES,
        IPSET_OPT_RESIZE,
        IPSET_OPT_SIZE,
        /* Create-specific options, filled out by the kernel */
        IPSET_OPT_ELEMENTS,
        IPSET_OPT_REFERENCES,
        IPSET_OPT_MEMSIZE,
        /* ADT-specific options */
        IPSET_OPT_ETHER,
        IPSET_OPT_NAME,
        IPSET_OPT_NAMEREF,
        IPSET_OPT_IP2,
        IPSET_OPT_CIDR2,
        IPSET_OPT_IP2_TO,
        IPSET_OPT_PROTO,
        IPSET_OPT_IFACE,
        /* Swap/rename to */
        IPSET_OPT_SETNAME2,
        /* Flags */
        IPSET_OPT_EXIST,
        IPSET_OPT_BEFORE,
        IPSET_OPT_PHYSDEV,
        IPSET_OPT_NOMATCH,
        IPSET_OPT_COUNTERS,
        IPSET_OPT_PACKETS,
        IPSET_OPT_BYTES,
        IPSET_OPT_CREATE_COMMENT,
        IPSET_OPT_ADT_COMMENT,
        /* Internal options */
        IPSET_OPT_FLAGS = 48,   /* IPSET_FLAG_EXIST| */
        IPSET_OPT_CADT_FLAGS,   /* IPSET_FLAG_BEFORE| */
        IPSET_OPT_ELEM,
        IPSET_OPT_TYPE,
        IPSET_OPT_LINENO,
        IPSET_OPT_REVISION,
        IPSET_OPT_REVISION_MIN,
        IPSET_OPT_MAX,
};
extern int ipset_data_set(struct ipset_data *data, enum ipset_opt opt,
                          const void *value);
extern const void *ipset_data_get(const struct ipset_data *data,
                                  enum ipset_opt opt);


/* standard library */
int printf(const char *format, ...);
"""

ffi = FFI()
ffi.cdef(cdef)
C = ffi.verify("""
#include <stdbool.h>                            /* bool */
#include <stdint.h>                             /* uintxx_t */
#include <stdio.h>                              /* printf */

#include <libipset/linux_ip_set.h>              /* enum ipset_cmd */
#include <libipset/data.h>    /* enum ipset_data */
#include <libipset/session.h>
#include <libipset/parse.h>   /* ipset_parse_* */
#include <libipset/types.h>   /* struct ipset_type */
#include <libipset/ui.h>    /* core options, commands */
#include <libipset/utils.h>   /* STREQ */

/* Report and output buffer sizes */
#define IPSET_ERRORBUFLEN               1024
#define IPSET_OUTBUFLEN                 8192

""", libraries=['ipset', 'mnl'])
