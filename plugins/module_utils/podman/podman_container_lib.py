from __future__ import (absolute_import, division, print_function)
import json  # noqa: F402
import os  # noqa: F402
import shlex  # noqa: F402

from ansible.module_utils._text import to_bytes, to_native  # noqa: F402
from ansible_collections.containers.podman.plugins.module_utils.podman.common import LooseVersion
from ansible_collections.containers.podman.plugins.module_utils.podman.common import lower_keys
from ansible_collections.containers.podman.plugins.module_utils.podman.common import generate_systemd
from ansible_collections.containers.podman.plugins.module_utils.podman.common import delete_systemd
from ansible_collections.containers.podman.plugins.module_utils.podman.common import normalize_signal
from ansible_collections.containers.podman.plugins.module_utils.podman.common import ARGUMENTS_OPTS_DICT

__metaclass__ = type

ARGUMENTS_SPEC_CONTAINER = dict(
    name=dict(required=True, type='str'),
    executable=dict(default='podman', type='str'),
    state=dict(type='str', default='started', choices=[
        'absent', 'present', 'stopped', 'started', 'created']),
    image=dict(type='str'),
    annotation=dict(type='dict'),
    attach=dict(type='list', elements='str', choices=['stdout', 'stderr', 'stdin']),
    authfile=dict(type='path'),
    blkio_weight=dict(type='int'),
    blkio_weight_device=dict(type='dict'),
    cap_add=dict(type='list', elements='str', aliases=['capabilities']),
    cap_drop=dict(type='list', elements='str'),
    cgroup_parent=dict(type='path'),
    cgroupns=dict(type='str'),
    cgroups=dict(type='str'),
    cidfile=dict(type='path'),
    cmd_args=dict(type='list', elements='str'),
    conmon_pidfile=dict(type='path'),
    command=dict(type='raw'),
    cpu_period=dict(type='int'),
    cpu_quota=dict(type='int'),
    cpu_rt_period=dict(type='int'),
    cpu_rt_runtime=dict(type='int'),
    cpu_shares=dict(type='int'),
    cpus=dict(type='str'),
    cpuset_cpus=dict(type='str'),
    cpuset_mems=dict(type='str'),
    delete_depend=dict(type='bool'),
    delete_time=dict(type='str'),
    delete_volumes=dict(type='bool'),
    detach=dict(type='bool', default=True),
    debug=dict(type='bool', default=False),
    detach_keys=dict(type='str', no_log=False),
    device=dict(type='list', elements='str'),
    device_read_bps=dict(type='list', elements='str'),
    device_read_iops=dict(type='list', elements='str'),
    device_write_bps=dict(type='list', elements='str'),
    device_write_iops=dict(type='list', elements='str'),
    dns=dict(type='list', elements='str', aliases=['dns_servers']),
    dns_option=dict(type='str', aliases=['dns_opts']),
    dns_search=dict(type='str', aliases=['dns_search_domains']),
    entrypoint=dict(type='str'),
    env=dict(type='dict'),
    env_file=dict(type='list', elements='path', aliases=['env_files']),
    env_host=dict(type='bool'),
    etc_hosts=dict(type='dict', aliases=['add_hosts']),
    expose=dict(type='list', elements='str', aliases=[
                'exposed', 'exposed_ports']),
    force_restart=dict(type='bool', default=False,
                       aliases=['restart']),
    force_delete=dict(type='bool', default=True),
    generate_systemd=dict(type='dict', default={}),
    gidmap=dict(type='list', elements='str'),
    group_add=dict(type='list', elements='str', aliases=['groups']),
    healthcheck=dict(type='str'),
    healthcheck_interval=dict(type='str'),
    healthcheck_retries=dict(type='int'),
    healthcheck_start_period=dict(type='str'),
    healthcheck_timeout=dict(type='str'),
    healthcheck_failure_action=dict(type='str', choices=[
        'none', 'kill', 'restart', 'stop']),
    hooks_dir=dict(type='list', elements='str'),
    hostname=dict(type='str'),
    http_proxy=dict(type='bool'),
    image_volume=dict(type='str', choices=['bind', 'tmpfs', 'ignore']),
    image_strict=dict(type='bool', default=False),
    init=dict(type='bool'),
    init_path=dict(type='str'),
    interactive=dict(type='bool'),
    ip=dict(type='str'),
    ipc=dict(type='str', aliases=['ipc_mode']),
    kernel_memory=dict(type='str'),
    label=dict(type='dict', aliases=['labels']),
    label_file=dict(type='str'),
    log_driver=dict(type='str', choices=[
        'k8s-file', 'journald', 'json-file']),
    log_level=dict(
        type='str',
        choices=["debug", "info", "warn", "error", "fatal", "panic"]),
    log_opt=dict(type='dict', aliases=['log_options'],
                 options=dict(
        max_size=dict(type='str'),
        path=dict(type='str'),
        tag=dict(type='str'))),
    mac_address=dict(type='str'),
    memory=dict(type='str'),
    memory_reservation=dict(type='str'),
    memory_swap=dict(type='str'),
    memory_swappiness=dict(type='int'),
    mount=dict(type='list', elements='str', aliases=['mounts']),
    network=dict(type='list', elements='str', aliases=['net', 'network_mode']),
    network_aliases=dict(type='list', elements='str'),
    no_hosts=dict(type='bool'),
    oom_kill_disable=dict(type='bool'),
    oom_score_adj=dict(type='int'),
    pid=dict(type='str', aliases=['pid_mode']),
    pids_limit=dict(type='str'),
    pod=dict(type='str'),
    privileged=dict(type='bool'),
    publish=dict(type='list', elements='str', aliases=[
        'ports', 'published', 'published_ports']),
    publish_all=dict(type='bool'),
    read_only=dict(type='bool'),
    read_only_tmpfs=dict(type='bool'),
    recreate=dict(type='bool', default=False),
    requires=dict(type='list', elements='str'),
    restart_policy=dict(type='str'),
    restart_time=dict(type='str'),
    rm=dict(type='bool', aliases=['remove', 'auto_remove']),
    rootfs=dict(type='bool'),
    secrets=dict(type='list', elements='str', no_log=True),
    sdnotify=dict(type='str'),
    security_opt=dict(type='list', elements='str'),
    shm_size=dict(type='str'),
    sig_proxy=dict(type='bool'),
    stop_signal=dict(type='int'),
    stop_timeout=dict(type='int'),
    stop_time=dict(type='str'),
    subgidname=dict(type='str'),
    subuidname=dict(type='str'),
    sysctl=dict(type='dict'),
    systemd=dict(type='str'),
    timezone=dict(type='str'),
    tmpfs=dict(type='dict'),
    tty=dict(type='bool'),
    uidmap=dict(type='list', elements='str'),
    ulimit=dict(type='list', elements='str', aliases=['ulimits']),
    user=dict(type='str'),
    userns=dict(type='str', aliases=['userns_mode']),
    uts=dict(type='str'),
    volume=dict(type='list', elements='str', aliases=['volumes']),
    volumes_from=dict(type='list', elements='str'),
    workdir=dict(type='str', aliases=['working_dir'])
)


def init_options():
    default = {}
    opts = ARGUMENTS_SPEC_CONTAINER
    for k, v in opts.items():
        if 'default' in v:
            default[k] = v['default']
        else:
            default[k] = None
    return default


def update_options(opts_dict, container):
    def to_bool(x):
        return str(x).lower() not in ['no', 'false']

    aliases = {}
    for k, v in ARGUMENTS_SPEC_CONTAINER.items():
        if 'aliases' in v:
            for alias in v['aliases']:
                aliases[alias] = k
    for k in list(container):
        if k in aliases:
            key = aliases[k]
            container[key] = container.pop(k)
        else:
            key = k
        if ARGUMENTS_SPEC_CONTAINER[key]['type'] == 'list' and not isinstance(container[key], list):
            opts_dict[key] = [container[key]]
        elif ARGUMENTS_SPEC_CONTAINER[key]['type'] == 'bool' and not isinstance(container[key], bool):
            opts_dict[key] = to_bool(container[key])
        elif ARGUMENTS_SPEC_CONTAINER[key]['type'] == 'int' and not isinstance(container[key], int):
            opts_dict[key] = int(container[key])
        else:
            opts_dict[key] = container[key]

    return opts_dict


def set_container_opts(input_vars):
    default_options_templ = init_options()
    options_dict = update_options(default_options_templ, input_vars)
    return options_dict


class PodmanModuleParams:
    """Creates list of arguments for podman CLI command.

       Arguments:
           action {str} -- action type from 'run', 'stop', 'create', 'delete',
                           'start', 'restart'
           params {dict} -- dictionary of module parameters

       """

    def __init__(self, action, params, podman_version, module):
        self.params = params
        self.action = action
        self.podman_version = podman_version
        self.module = module

    def construct_command_from_params(self):
        """Create a podman command from given module parameters.

        Returns:
           list -- list of byte strings for Popen command
        """
        if self.action in ['start', 'stop', 'delete', 'restart']:
            return self.start_stop_delete()
        if self.action in ['create', 'run']:
            cmd = [self.action, '--name', self.params['name']]
            all_param_methods = [func for func in dir(self)
                                 if callable(getattr(self, func))
                                 and func.startswith("addparam")]
            params_set = (i for i in self.params if self.params[i] is not None)
            for param in params_set:
                func_name = "_".join(["addparam", param])
                if func_name in all_param_methods:
                    cmd = getattr(self, func_name)(cmd)
            cmd.append(self.params['image'])
            if self.params['command']:
                if isinstance(self.params['command'], list):
                    cmd += self.params['command']
                else:
                    cmd += self.params['command'].split()
            return [to_bytes(i, errors='surrogate_or_strict') for i in cmd]

    def start_stop_delete(self):

        def complete_params(cmd):
            if self.params['attach'] and self.action == 'start':
                cmd.append('--attach')
            if self.params['detach'] is False and self.action == 'start' and '--attach' not in cmd:
                cmd.append('--attach')
            if self.params['detach_keys'] and self.action == 'start':
                cmd += ['--detach-keys', self.params['detach_keys']]
            if self.params['sig_proxy'] and self.action == 'start':
                cmd.append('--sig-proxy')
            if self.params['stop_time'] and self.action == 'stop':
                cmd += ['--time', self.params['stop_time']]
            if self.params['restart_time'] and self.action == 'restart':
                cmd += ['--time', self.params['restart_time']]
            if self.params['delete_depend'] and self.action == 'delete':
                cmd.append('--depend')
            if self.params['delete_time'] and self.action == 'delete':
                cmd += ['--time', self.params['delete_time']]
            if self.params['delete_volumes'] and self.action == 'delete':
                cmd.append('--volumes')
            if self.params['force_delete'] and self.action == 'delete':
                cmd.append('--force')
            return cmd

        if self.action in ['stop', 'start', 'restart']:
            cmd = complete_params([self.action]) + [self.params['name']]
            return [to_bytes(i, errors='surrogate_or_strict') for i in cmd]

        if self.action == 'delete':
            cmd = complete_params(['rm']) + [self.params['name']]
            return [to_bytes(i, errors='surrogate_or_strict') for i in cmd]

    def check_version(self, param, minv=None, maxv=None):
        if minv and LooseVersion(minv) > LooseVersion(
                self.podman_version):
            self.module.fail_json(msg="Parameter %s is supported from podman "
                                  "version %s only! Current version is %s" % (
                                      param, minv, self.podman_version))
        if maxv and LooseVersion(maxv) < LooseVersion(
                self.podman_version):
            self.module.fail_json(msg="Parameter %s is supported till podman "
                                  "version %s only! Current version is %s" % (
                                      param, minv, self.podman_version))

    def addparam_annotation(self, c):
        for annotate in self.params['annotation'].items():
            c += ['--annotation', '='.join(annotate)]
        return c

    def addparam_attach(self, c):
        for attach in self.params['attach']:
            c += ['--attach=%s' % attach]
        return c

    def addparam_authfile(self, c):
        return c + ['--authfile', self.params['authfile']]

    def addparam_blkio_weight(self, c):
        return c + ['--blkio-weight', self.params['blkio_weight']]

    def addparam_blkio_weight_device(self, c):
        for blkio in self.params['blkio_weight_device'].items():
            c += ['--blkio-weight-device', ':'.join(blkio)]
        return c

    def addparam_cap_add(self, c):
        for cap_add in self.params['cap_add']:
            c += ['--cap-add', cap_add]
        return c

    def addparam_cap_drop(self, c):
        for cap_drop in self.params['cap_drop']:
            c += ['--cap-drop', cap_drop]
        return c

    def addparam_cgroups(self, c):
        self.check_version('--cgroups', minv='1.6.0')
        return c + ['--cgroups=%s' % self.params['cgroups']]

    def addparam_cgroupns(self, c):
        self.check_version('--cgroupns', minv='1.6.2')
        return c + ['--cgroupns=%s' % self.params['cgroupns']]

    def addparam_cgroup_parent(self, c):
        return c + ['--cgroup-parent', self.params['cgroup_parent']]

    def addparam_cidfile(self, c):
        return c + ['--cidfile', self.params['cidfile']]

    def addparam_conmon_pidfile(self, c):
        return c + ['--conmon-pidfile', self.params['conmon_pidfile']]

    def addparam_cpu_period(self, c):
        return c + ['--cpu-period', self.params['cpu_period']]

    def addparam_cpu_quota(self, c):
        return c + ['--cpu-quota', self.params['cpu_quota']]

    def addparam_cpu_rt_period(self, c):
        return c + ['--cpu-rt-period', self.params['cpu_rt_period']]

    def addparam_cpu_rt_runtime(self, c):
        return c + ['--cpu-rt-runtime', self.params['cpu_rt_runtime']]

    def addparam_cpu_shares(self, c):
        return c + ['--cpu-shares', self.params['cpu_shares']]

    def addparam_cpus(self, c):
        return c + ['--cpus', self.params['cpus']]

    def addparam_cpuset_cpus(self, c):
        return c + ['--cpuset-cpus', self.params['cpuset_cpus']]

    def addparam_cpuset_mems(self, c):
        return c + ['--cpuset-mems', self.params['cpuset_mems']]

    def addparam_detach(self, c):
        # Remove detach from create command and don't set if attach is true
        if self.action == 'create' or self.params['attach']:
            return c
        return c + ['--detach=%s' % self.params['detach']]

    def addparam_detach_keys(self, c):
        return c + ['--detach-keys', self.params['detach_keys']]

    def addparam_device(self, c):
        for dev in self.params['device']:
            c += ['--device', dev]
        return c

    def addparam_device_read_bps(self, c):
        for dev in self.params['device_read_bps']:
            c += ['--device-read-bps', dev]
        return c

    def addparam_device_read_iops(self, c):
        for dev in self.params['device_read_iops']:
            c += ['--device-read-iops', dev]
        return c

    def addparam_device_write_bps(self, c):
        for dev in self.params['device_write_bps']:
            c += ['--device-write-bps', dev]
        return c

    def addparam_device_write_iops(self, c):
        for dev in self.params['device_write_iops']:
            c += ['--device-write-iops', dev]
        return c

    def addparam_dns(self, c):
        return c + ['--dns', ','.join(self.params['dns'])]

    def addparam_dns_option(self, c):
        return c + ['--dns-option', self.params['dns_option']]

    def addparam_dns_search(self, c):
        return c + ['--dns-search', self.params['dns_search']]

    def addparam_entrypoint(self, c):
        return c + ['--entrypoint', self.params['entrypoint']]

    def addparam_env(self, c):
        for env_value in self.params['env'].items():
            c += ['--env',
                  b"=".join([to_bytes(k, errors='surrogate_or_strict')
                             for k in env_value])]
        return c

    def addparam_env_file(self, c):
        for env_file in self.params['env_file']:
            c += ['--env-file', env_file]
        return c

    def addparam_env_host(self, c):
        self.check_version('--env-host', minv='1.5.0')
        return c + ['--env-host=%s' % self.params['env_host']]

    def addparam_etc_hosts(self, c):
        for host_ip in self.params['etc_hosts'].items():
            c += ['--add-host', ':'.join(host_ip)]
        return c

    def addparam_expose(self, c):
        for exp in self.params['expose']:
            c += ['--expose', exp]
        return c

    def addparam_gidmap(self, c):
        for gidmap in self.params['gidmap']:
            c += ['--gidmap', gidmap]
        return c

    def addparam_group_add(self, c):
        for g in self.params['group_add']:
            c += ['--group-add', g]
        return c

    def addparam_healthcheck(self, c):
        return c + ['--healthcheck-command', self.params['healthcheck']]

    def addparam_healthcheck_interval(self, c):
        return c + ['--healthcheck-interval',
                    self.params['healthcheck_interval']]

    def addparam_healthcheck_retries(self, c):
        return c + ['--healthcheck-retries',
                    self.params['healthcheck_retries']]

    def addparam_healthcheck_start_period(self, c):
        return c + ['--healthcheck-start-period',
                    self.params['healthcheck_start_period']]

    def addparam_healthcheck_timeout(self, c):
        return c + ['--healthcheck-timeout',
                    self.params['healthcheck_timeout']]

    def addparam_healthcheck_failure_action(self, c):
        return c + ['--health-on-failure',
                    self.params['healthcheck_failure_action']]

    def addparam_hooks_dir(self, c):
        for hook_dir in self.params['hooks_dir']:
            c += ['--hooks-dir=%s' % hook_dir]
        return c

    def addparam_hostname(self, c):
        return c + ['--hostname', self.params['hostname']]

    def addparam_http_proxy(self, c):
        return c + ['--http-proxy=%s' % self.params['http_proxy']]

    def addparam_image_volume(self, c):
        return c + ['--image-volume', self.params['image_volume']]

    def addparam_init(self, c):
        if self.params['init']:
            c += ['--init']
        return c

    def addparam_init_path(self, c):
        return c + ['--init-path', self.params['init_path']]

    def addparam_interactive(self, c):
        return c + ['--interactive=%s' % self.params['interactive']]

    def addparam_ip(self, c):
        return c + ['--ip', self.params['ip']]

    def addparam_ipc(self, c):
        return c + ['--ipc', self.params['ipc']]

    def addparam_kernel_memory(self, c):
        return c + ['--kernel-memory', self.params['kernel_memory']]

    def addparam_label(self, c):
        for label in self.params['label'].items():
            c += ['--label', b'='.join([to_bytes(la, errors='surrogate_or_strict')
                                        for la in label])]
        return c

    def addparam_label_file(self, c):
        return c + ['--label-file', self.params['label_file']]

    def addparam_log_driver(self, c):
        return c + ['--log-driver', self.params['log_driver']]

    def addparam_log_opt(self, c):
        for k, v in self.params['log_opt'].items():
            if v is not None:
                c += ['--log-opt',
                      b"=".join([to_bytes(k.replace('max_size', 'max-size'),
                                          errors='surrogate_or_strict'),
                                 to_bytes(v,
                                          errors='surrogate_or_strict')])]
        return c

    def addparam_log_level(self, c):
        return c + ['--log-level', self.params['log_level']]

    def addparam_mac_address(self, c):
        return c + ['--mac-address', self.params['mac_address']]

    def addparam_memory(self, c):
        return c + ['--memory', self.params['memory']]

    def addparam_memory_reservation(self, c):
        return c + ['--memory-reservation', self.params['memory_reservation']]

    def addparam_memory_swap(self, c):
        return c + ['--memory-swap', self.params['memory_swap']]

    def addparam_memory_swappiness(self, c):
        return c + ['--memory-swappiness', self.params['memory_swappiness']]

    def addparam_mount(self, c):
        for mnt in self.params['mount']:
            if mnt:
                c += ['--mount', mnt]
        return c

    def addparam_network(self, c):
        if LooseVersion(self.podman_version) >= LooseVersion('4.0.0'):
            for net in self.params['network']:
                c += ['--network', net]
            return c
        return c + ['--network', ",".join(self.params['network'])]

    def addparam_network_aliases(self, c):
        for alias in self.params['network_aliases']:
            c += ['--network-alias', alias]
        return c

    def addparam_no_hosts(self, c):
        return c + ['--no-hosts=%s' % self.params['no_hosts']]

    def addparam_oom_kill_disable(self, c):
        return c + ['--oom-kill-disable=%s' % self.params['oom_kill_disable']]

    def addparam_oom_score_adj(self, c):
        return c + ['--oom-score-adj', self.params['oom_score_adj']]

    def addparam_pid(self, c):
        return c + ['--pid', self.params['pid']]

    def addparam_pids_limit(self, c):
        return c + ['--pids-limit', self.params['pids_limit']]

    def addparam_pod(self, c):
        return c + ['--pod', self.params['pod']]

    def addparam_privileged(self, c):
        return c + ['--privileged=%s' % self.params['privileged']]

    def addparam_publish(self, c):
        for pub in self.params['publish']:
            c += ['--publish', pub]
        return c

    def addparam_publish_all(self, c):
        return c + ['--publish-all=%s' % self.params['publish_all']]

    def addparam_read_only(self, c):
        return c + ['--read-only=%s' % self.params['read_only']]

    def addparam_read_only_tmpfs(self, c):
        return c + ['--read-only-tmpfs=%s' % self.params['read_only_tmpfs']]

    def addparam_requires(self, c):
        return c + ['--requires', ",".join(self.params['requires'])]

    def addparam_restart_policy(self, c):
        return c + ['--restart=%s' % self.params['restart_policy']]

    def addparam_rm(self, c):
        if self.params['rm']:
            c += ['--rm']
        return c

    def addparam_rootfs(self, c):
        return c + ['--rootfs=%s' % self.params['rootfs']]

    def addparam_sdnotify(self, c):
        return c + ['--sdnotify=%s' % self.params['sdnotify']]

    def addparam_secrets(self, c):
        for secret in self.params['secrets']:
            c += ['--secret', secret]
        return c

    def addparam_security_opt(self, c):
        for secopt in self.params['security_opt']:
            c += ['--security-opt', secopt]
        return c

    def addparam_shm_size(self, c):
        return c + ['--shm-size', self.params['shm_size']]

    def addparam_sig_proxy(self, c):
        return c + ['--sig-proxy=%s' % self.params['sig_proxy']]

    def addparam_stop_signal(self, c):
        return c + ['--stop-signal', self.params['stop_signal']]

    def addparam_stop_timeout(self, c):
        return c + ['--stop-timeout', self.params['stop_timeout']]

    def addparam_subgidname(self, c):
        return c + ['--subgidname', self.params['subgidname']]

    def addparam_subuidname(self, c):
        return c + ['--subuidname', self.params['subuidname']]

    def addparam_sysctl(self, c):
        for sysctl in self.params['sysctl'].items():
            c += ['--sysctl',
                  b"=".join([to_bytes(k, errors='surrogate_or_strict')
                             for k in sysctl])]
        return c

    def addparam_systemd(self, c):
        return c + ['--systemd=%s' % str(self.params['systemd']).lower()]

    def addparam_tmpfs(self, c):
        for tmpfs in self.params['tmpfs'].items():
            c += ['--tmpfs', ':'.join(tmpfs)]
        return c

    def addparam_timezone(self, c):
        return c + ['--tz=%s' % self.params['timezone']]

    def addparam_tty(self, c):
        return c + ['--tty=%s' % self.params['tty']]

    def addparam_uidmap(self, c):
        for uidmap in self.params['uidmap']:
            c += ['--uidmap', uidmap]
        return c

    def addparam_ulimit(self, c):
        for u in self.params['ulimit']:
            c += ['--ulimit', u]
        return c

    def addparam_user(self, c):
        return c + ['--user', self.params['user']]

    def addparam_userns(self, c):
        return c + ['--userns', self.params['userns']]

    def addparam_uts(self, c):
        return c + ['--uts', self.params['uts']]

    def addparam_volume(self, c):
        for vol in self.params['volume']:
            if vol:
                c += ['--volume', vol]
        return c

    def addparam_volumes_from(self, c):
        for vol in self.params['volumes_from']:
            c += ['--volumes-from', vol]
        return c

    def addparam_workdir(self, c):
        return c + ['--workdir', self.params['workdir']]

    # Add your own args for podman command
    def addparam_cmd_args(self, c):
        return c + self.params['cmd_args']


class PodmanDefaults:
    def __init__(self, image_info, podman_version):
        self.version = podman_version
        self.image_info = image_info
        self.defaults = {
            "blkio_weight": 0,
            "cgroups": "default",
            "cidfile": "",
            "cpus": 0.0,
            "cpu_shares": 0,
            "cpu_quota": 0,
            "cpu_period": 0,
            "cpu_rt_runtime": 0,
            "cpu_rt_period": 0,
            "cpuset_cpus": "",
            "cpuset_mems": "",
            "detach": True,
            "device": [],
            "env_host": False,
            "etc_hosts": {},
            "group_add": [],
            "ipc": "",
            "kernelmemory": "0",
            "log_level": "error",
            "memory": "0",
            "memory_swap": "0",
            "memory_reservation": "0",
            # "memory_swappiness": -1,
            "no_hosts": False,
            # libpod issue with networks in inspection
            "oom_score_adj": 0,
            "pid": "",
            "privileged": False,
            "read_only": False,
            "rm": False,
            "security_opt": [],
            "stop_signal": self.image_info.get('config', {}).get('stopsignal', "15"),
            "tty": False,
            "user": self.image_info.get('user', ''),
            "workdir": self.image_info.get('config', {}).get('workingdir', '/'),
            "uts": "",
        }

    def default_dict(self):
        # make here any changes to self.defaults related to podman version
        # https://github.com/containers/libpod/pull/5669
        if (LooseVersion(self.version) >= LooseVersion('1.8.0')
                and LooseVersion(self.version) < LooseVersion('1.9.0')):
            self.defaults['cpu_shares'] = 1024
        if (LooseVersion(self.version) >= LooseVersion('2.0.0')):
            self.defaults['network'] = ["slirp4netns"]
            self.defaults['ipc'] = "private"
            self.defaults['uts'] = "private"
            self.defaults['pid'] = "private"
        if (LooseVersion(self.version) >= LooseVersion('3.0.0')):
            self.defaults['log_level'] = "warning"
        if (LooseVersion(self.version) >= LooseVersion('4.1.0')):
            self.defaults['ipc'] = "shareable"
        return self.defaults


class PodmanContainerDiff:
    def __init__(self, module, module_params, info, image_info, podman_version):
        self.module = module
        self.module_params = module_params
        self.version = podman_version
        self.default_dict = None
        self.info = lower_keys(info)
        self.image_info = lower_keys(image_info)
        self.params = self.defaultize()
        self.diff = {'before': {}, 'after': {}}
        self.non_idempotent = {}

    def defaultize(self):
        params_with_defaults = {}
        self.default_dict = PodmanDefaults(
            self.image_info, self.version).default_dict()
        for p in self.module_params:
            if self.module_params[p] is None and p in self.default_dict:
                params_with_defaults[p] = self.default_dict[p]
            else:
                params_with_defaults[p] = self.module_params[p]
        return params_with_defaults

    def _createcommand(self, argument):
        """Returns list of values for given argument from CreateCommand
        from Podman container inspect output.

        Args:
            argument (str): argument name

        Returns:

            all_values: list of values for given argument from createcommand
        """
        if "createcommand" not in self.info["config"]:
            return []
        cr_com = self.info["config"]["createcommand"]
        argument_values = ARGUMENTS_OPTS_DICT.get(argument, [argument])
        all_values = []
        for arg in argument_values:
            for ind, cr_opt in enumerate(cr_com):
                if arg == cr_opt:
                    # This is a key=value argument
                    if not cr_com[ind + 1].startswith("-"):
                        all_values.append(cr_com[ind + 1])
                    else:
                        # This is a false/true switching argument
                        return [True]
                if cr_opt.startswith("%s=" % arg):
                    all_values.append(cr_opt.split("=", 1)[1])
        return all_values

    def _diff_update_and_compare(self, param_name, before, after):
        if before != after:
            self.diff['before'].update({param_name: before})
            self.diff['after'].update({param_name: after})
            return True
        return False

    def _clean_path(self, x):
        '''Remove trailing and double slashes from path.'''
        if not x.rstrip("/"):
            return "/"
        return x.replace("//", "/").rstrip("/")

    def _clean_path_in_mount_str(self, mounts):
        mfin = []
        for mstr in mounts:
            for mitem in mstr.split(','):
                nv = mitem.split('=', maxsplit=1)
                miname = nv[0]
                mival = nv[1] if len(nv) > 1 else None
                if miname in ['src', 'source', 'dst', 'dest', 'destination', 'target']:
                    if mival:
                        mival = self._clean_path(mival)
                if mival is None:
                    mfin.append(miname)
                else:
                    mfin.append("{0}={1}".format(miname, mival))
        return mfin

    def diffparam_annotation(self):
        before = self.info['config']['annotations'] or {}
        after = before.copy()
        if self.module_params['annotation'] is not None:
            after.update(self.params['annotation'])
        return self._diff_update_and_compare('annotation', before, after)

    def diffparam_env_host(self):
        # It's impossible to get from inspect, recreate it if not default
        before = False
        after = self.params['env_host']
        return self._diff_update_and_compare('env_host', before, after)

    def diffparam_blkio_weight(self):
        before = self.info['hostconfig']['blkioweight']
        after = self.params['blkio_weight']
        return self._diff_update_and_compare('blkio_weight', before, after)

    def diffparam_blkio_weight_device(self):
        before = self.info['hostconfig']['blkioweightdevice']
        if before == [] and self.module_params['blkio_weight_device'] is None:
            after = []
        else:
            after = self.params['blkio_weight_device']
        return self._diff_update_and_compare('blkio_weight_device', before, after)

    def diffparam_cap_add(self):
        before = self.info['effectivecaps'] or []
        before = [i.lower() for i in before]
        after = []
        if self.module_params['cap_add'] is not None:
            for cap in self.module_params['cap_add']:
                cap = cap.lower()
                cap = cap if cap.startswith('cap_') else 'cap_' + cap
                after.append(cap)
        after += before
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('cap_add', before, after)

    def diffparam_cap_drop(self):
        before = self.info['effectivecaps'] or []
        before = [i.lower() for i in before]
        after = before[:]
        if self.module_params['cap_drop'] is not None:
            for cap in self.module_params['cap_drop']:
                cap = cap.lower()
                cap = cap if cap.startswith('cap_') else 'cap_' + cap
                if cap in after:
                    after.remove(cap)
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('cap_drop', before, after)

    def diffparam_cgroup_parent(self):
        before = self.info['hostconfig']['cgroupparent']
        after = self.params['cgroup_parent']
        if after is None:
            after = before
        return self._diff_update_and_compare('cgroup_parent', before, after)

    def diffparam_cgroups(self):
        # Cgroups output is not supported in all versions
        if 'cgroups' in self.info['hostconfig']:
            before = self.info['hostconfig']['cgroups']
            after = self.params['cgroups']
            return self._diff_update_and_compare('cgroups', before, after)
        return False

    def diffparam_cidfile(self):
        before = self.info['hostconfig']['containeridfile']
        after = self.params['cidfile']
        labels = self.info['config']['labels'] or {}
        # Ignore cidfile that is coming from systemd files
        # https://github.com/containers/ansible-podman-collections/issues/276
        if 'podman_systemd_unit' in labels:
            after = before
        return self._diff_update_and_compare('cidfile', before, after)

    def diffparam_command(self):
        # TODO(sshnaidm): to inspect image to get the default command
        if self.module_params['command'] is not None:
            before = self.info['config']['cmd']
            after = self.params['command']
            if isinstance(after, str):
                after = shlex.split(after)
            return self._diff_update_and_compare('command', before, after)
        return False

    def diffparam_conmon_pidfile(self):
        before = self.info['conmonpidfile']
        if self.module_params['conmon_pidfile'] is None:
            after = before
        else:
            after = self.params['conmon_pidfile']
        return self._diff_update_and_compare('conmon_pidfile', before, after)

    def diffparam_cpu_period(self):
        before = self.info['hostconfig']['cpuperiod']
        # if cpu_period left to default keep settings
        after = self.params['cpu_period'] or before
        return self._diff_update_and_compare('cpu_period', before, after)

    def diffparam_cpu_quota(self):
        before = self.info['hostconfig']['cpuquota']
        # if cpu_quota left to default keep settings
        after = self.params['cpu_quota'] or before
        return self._diff_update_and_compare('cpu_quota', before, after)

    def diffparam_cpu_rt_period(self):
        before = self.info['hostconfig']['cpurealtimeperiod']
        after = self.params['cpu_rt_period']
        return self._diff_update_and_compare('cpu_rt_period', before, after)

    def diffparam_cpu_rt_runtime(self):
        before = self.info['hostconfig']['cpurealtimeruntime']
        after = self.params['cpu_rt_runtime']
        return self._diff_update_and_compare('cpu_rt_runtime', before, after)

    def diffparam_cpu_shares(self):
        before = self.info['hostconfig']['cpushares']
        after = self.params['cpu_shares']
        return self._diff_update_and_compare('cpu_shares', before, after)

    def diffparam_cpus(self):
        before = self.info['hostconfig']['nanocpus'] / 1000000000
        # if cpus left to default keep settings
        after = float(self.params['cpus'] or before)
        return self._diff_update_and_compare('cpus', before, after)

    def diffparam_cpuset_cpus(self):
        before = self.info['hostconfig']['cpusetcpus']
        after = self.params['cpuset_cpus']
        return self._diff_update_and_compare('cpuset_cpus', before, after)

    def diffparam_cpuset_mems(self):
        before = self.info['hostconfig']['cpusetmems']
        after = self.params['cpuset_mems']
        return self._diff_update_and_compare('cpuset_mems', before, after)

    def diffparam_device(self):
        before = [":".join([i['pathonhost'], i['pathincontainer']])
                  for i in self.info['hostconfig']['devices']]
        if not before and 'createcommand' in self.info['config']:
            before = [i.lower() for i in self._createcommand('--device')]
        before = [":".join((i, i))
                  if len(i.split(":")) == 1 else i for i in before]
        after = [":".join(i.split(":")[:2]) for i in self.params['device']]
        after = [":".join((i, i))
                 if len(i.split(":")) == 1 else i for i in after]
        before, after = [i.lower() for i in before], [i.lower() for i in after]
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('devices', before, after)

    def diffparam_device_read_bps(self):
        before = self.info['hostconfig']['blkiodevicereadbps'] or []
        before = ["%s:%s" % (i['path'], i['rate']) for i in before]
        after = self.params['device_read_bps'] or []
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('device_read_bps', before, after)

    def diffparam_device_read_iops(self):
        before = self.info['hostconfig']['blkiodevicereadiops'] or []
        before = ["%s:%s" % (i['path'], i['rate']) for i in before]
        after = self.params['device_read_iops'] or []
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('device_read_iops', before, after)

    def diffparam_device_write_bps(self):
        before = self.info['hostconfig']['blkiodevicewritebps'] or []
        before = ["%s:%s" % (i['path'], i['rate']) for i in before]
        after = self.params['device_write_bps'] or []
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('device_write_bps', before, after)

    def diffparam_device_write_iops(self):
        before = self.info['hostconfig']['blkiodevicewriteiops'] or []
        before = ["%s:%s" % (i['path'], i['rate']) for i in before]
        after = self.params['device_write_iops'] or []
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('device_write_iops', before, after)

    # Limited idempotency, it can't guess default values
    def diffparam_env(self):
        env_before = self.info['config']['env'] or {}
        before = {i.split("=")[0]: "=".join(i.split("=")[1:])
                  for i in env_before}
        after = before.copy()
        if self.params['env']:
            after.update({k: str(v) for k, v in self.params['env'].items()})
        return self._diff_update_and_compare('env', before, after)

    def diffparam_etc_hosts(self):
        if self.info['hostconfig']['extrahosts']:
            before = dict([i.split(":", 1)
                           for i in self.info['hostconfig']['extrahosts']])
        else:
            before = {}
        after = self.params['etc_hosts']
        return self._diff_update_and_compare('etc_hosts', before, after)

    def diffparam_group_add(self):
        before = self.info['hostconfig']['groupadd']
        after = self.params['group_add']
        return self._diff_update_and_compare('group_add', before, after)

    # Healthcheck is only defined in container config if a healthcheck
    # was configured; otherwise the config key isn't part of the config.
    def diffparam_healthcheck(self):
        before = ''
        if 'healthcheck' in self.info['config']:
            # the "test" key is a list of 2 items where the first one is
            # "CMD-SHELL" and the second one is the actual healthcheck command.
            if len(self.info['config']['healthcheck']['test']) > 1:
                before = self.info['config']['healthcheck']['test'][1]
        after = self.params['healthcheck'] or before
        return self._diff_update_and_compare('healthcheck', before, after)

    def diffparam_healthcheck_failure_action(self):
        if 'healthcheckonfailureaction' in self.info['config']:
            before = self.info['config']['healthcheckonfailureaction']
        else:
            before = ''
        after = self.params['healthcheck_failure_action'] or before
        return self._diff_update_and_compare('healthcheckonfailureaction', before, after)

    # Because of hostname is random generated, this parameter has partial idempotency only.
    def diffparam_hostname(self):
        before = self.info['config']['hostname']
        after = self.params['hostname'] or before
        return self._diff_update_and_compare('hostname', before, after)

    def diffparam_image(self):
        before_id = self.info['image'] or self.info['rootfs']
        after_id = self.image_info['id']
        if before_id == after_id:
            return self._diff_update_and_compare('image', before_id, after_id)
        is_rootfs = self.info['rootfs'] != '' or self.params['rootfs']
        before = self.info['config']['image'] or before_id
        after = self.params['image']
        mode = self.params['image_strict'] or is_rootfs
        if mode is None or not mode:
            # In a idempotency 'lite mode' assume all images from different registries are the same
            before = before.replace(":latest", "")
            after = after.replace(":latest", "")
            before = before.split("/")[-1]
            after = after.split("/")[-1]
        else:
            return self._diff_update_and_compare('image', before_id, after_id)
        return self._diff_update_and_compare('image', before, after)

    def diffparam_ipc(self):
        before = self.info['hostconfig']['ipcmode']
        after = self.params['ipc']
        if self.params['pod'] and not self.module_params['ipc']:
            after = before
        return self._diff_update_and_compare('ipc', before, after)

    def diffparam_label(self):
        before = self.info['config']['labels'] or {}
        after = self.image_info.get('labels') or {}
        if self.params['label']:
            after.update({
                str(k).lower(): str(v)
                for k, v in self.params['label'].items()
            })
        # Strip out labels that are coming from systemd files
        # https://github.com/containers/ansible-podman-collections/issues/276
        if 'podman_systemd_unit' in before:
            after.pop('podman_systemd_unit', None)
            before.pop('podman_systemd_unit', None)
        return self._diff_update_and_compare('label', before, after)

    def diffparam_log_driver(self):
        before = self.info['hostconfig']['logconfig']['type']
        if self.module_params['log_driver'] is not None:
            after = self.params['log_driver']
        else:
            after = before
        return self._diff_update_and_compare('log_driver', before, after)

    # Parameter has limited idempotency, unable to guess the default log_path
    def diffparam_log_opt(self):
        before, after = {}, {}

        # Log path
        path_before = None
        if 'logpath' in self.info:
            path_before = self.info['logpath']
        # For Podman v3
        if ('logconfig' in self.info['hostconfig'] and
                'path' in self.info['hostconfig']['logconfig']):
            path_before = self.info['hostconfig']['logconfig']['path']
        if path_before is not None:
            if (self.module_params['log_opt'] and
                    'path' in self.module_params['log_opt'] and
                    self.module_params['log_opt']['path'] is not None):
                path_after = self.params['log_opt']['path']
            else:
                path_after = path_before
            if path_before != path_after:
                before.update({'log-path': path_before})
                after.update({'log-path': path_after})

        # Log tag
        tag_before = None
        if 'logtag' in self.info:
            tag_before = self.info['logtag']
        # For Podman v3
        if ('logconfig' in self.info['hostconfig'] and
                'tag' in self.info['hostconfig']['logconfig']):
            tag_before = self.info['hostconfig']['logconfig']['tag']
        if tag_before is not None:
            if (self.module_params['log_opt'] and
                    'tag' in self.module_params['log_opt'] and
                    self.module_params['log_opt']['tag'] is not None):
                tag_after = self.params['log_opt']['tag']
            else:
                tag_after = ''
            if tag_before != tag_after:
                before.update({'log-tag': tag_before})
                after.update({'log-tag': tag_after})

        # Log size
        # For Podman v3
        # size_before = '0B'
        # TODO(sshnaidm): integrate B/KB/MB/GB calculation for sizes
        # if ('logconfig' in self.info['hostconfig'] and
        #         'size' in self.info['hostconfig']['logconfig']):
        #     size_before = self.info['hostconfig']['logconfig']['size']
        # if size_before != '0B':
        #     if (self.module_params['log_opt'] and
        #             'max_size' in self.module_params['log_opt'] and
        #             self.module_params['log_opt']['max_size'] is not None):
        #         size_after = self.params['log_opt']['max_size']
        #     else:
        #         size_after = ''
        #     if size_before != size_after:
        #         before.update({'log-size': size_before})
        #         after.update({'log-size': size_after})

        return self._diff_update_and_compare('log_opt', before, after)

    def diffparam_mac_address(self):
        before = str(self.info['networksettings']['macaddress'])
        if not before and self.info['networksettings'].get('networks'):
            nets = self.info['networksettings']['networks']
            macs = [
                nets[i]["macaddress"] for i in nets if nets[i]["macaddress"]]
            if macs:
                before = macs[0]
        if not before and 'createcommand' in self.info['config']:
            before = [i.lower() for i in self._createcommand('--mac-address')]
            before = before[0] if before else ''
        if self.module_params['mac_address'] is not None:
            after = self.params['mac_address']
        else:
            after = before
        return self._diff_update_and_compare('mac_address', before, after)

    def diffparam_mount(self):
        before = []
        if self.info['config'].get('createcommand'):
            cr_com = self.info['config']['createcommand']
            for i, v in enumerate(cr_com):
                if v == '--mount':
                    before = self._clean_path_in_mount_str(cr_com[i + 1])
        after = self.params.get('mount')
        if not after:
            after = []
        else:
            after = self._clean_path_in_mount_str(after)
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('mount', before, after)

    def diffparam_network(self):
        net_mode_before = self.info['hostconfig']['networkmode']
        net_mode_after = ''
        before = list(self.info['networksettings'].get('networks', {}))
        # Remove default 'podman' network in v3 for comparison
        if before == ['podman']:
            before = []
        # Special case for options for slirp4netns rootless networking from v2
        if net_mode_before == 'slirp4netns' and 'createcommand' in self.info['config']:
            cr_net = [i.lower() for i in self._createcommand('--network')]
            for cr_net_opt in cr_net:
                if 'slirp4netns:' in cr_net_opt:
                    before = [cr_net_opt]
        after = self.params['network'] or []
        # If container is in pod and no networks are provided
        if not self.module_params['network'] and self.params['pod']:
            after = before
            return self._diff_update_and_compare('network', before, after)
        # Check special network modes
        if after in [['bridge'], ['host'], ['slirp4netns'], ['none']]:
            net_mode_after = after[0]
        # If changes are only for network mode and container has no networks
        if net_mode_after and not before:
            # Remove differences between v1 and v2
            net_mode_after = net_mode_after.replace('bridge', 'default')
            net_mode_after = net_mode_after.replace('slirp4netns', 'default')
            net_mode_before = net_mode_before.replace('bridge', 'default')
            net_mode_before = net_mode_before.replace('slirp4netns', 'default')
            return self._diff_update_and_compare('network', net_mode_before, net_mode_after)
        # If container is attached to network of a different container
        if "container" in net_mode_before:
            for netw in after:
                if "container" in netw:
                    before = after = netw
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('network', before, after)

    def diffparam_oom_score_adj(self):
        before = self.info['hostconfig']['oomscoreadj']
        after = self.params['oom_score_adj']
        return self._diff_update_and_compare('oom_score_adj', before, after)

    def diffparam_privileged(self):
        before = self.info['hostconfig']['privileged']
        after = self.params['privileged']
        return self._diff_update_and_compare('privileged', before, after)

    def diffparam_pid(self):
        def get_container_id_by_name(name):
            rc, podman_inspect_info, err = self.module.run_command(
                [self.module.params["executable"], "inspect", name, "-f", "{{.Id}}"])
            if rc != 0:
                return None
            return podman_inspect_info.strip()

        before = self.info['hostconfig']['pidmode']
        after = self.params['pid']
        if after is not None and "container:" in after and "container:" in before:
            if after.split(":")[1] == before.split(":")[1]:
                return self._diff_update_and_compare('pid', before, after)
            after = "container:" + get_container_id_by_name(after.split(":")[1])
        return self._diff_update_and_compare('pid', before, after)

    # TODO(sshnaidm) Need to add port ranges support
    def diffparam_publish(self):
        def compose(p, h):
            s = ":".join(
                [str(h["hostport"]), p.replace('/tcp', '')]
            ).strip(":")
            if h['hostip']:
                return ":".join([h['hostip'], s])
            return s

        ports = self.info['hostconfig']['portbindings']
        before = []
        for port, hosts in ports.items():
            if hosts:
                for h in hosts:
                    before.append(compose(port, h))
        after = self.params['publish'] or []
        if self.params['publish_all']:
            image_ports = self.image_info.get('config', {}).get('exposedports', {})
            if image_ports:
                after += list(image_ports.keys())
        after = [
            i.replace("/tcp", "").replace("[", "").replace("]", "").replace("0.0.0.0:", "")
            for i in after]
        # No support for port ranges yet
        for ports in after:
            if "-" in ports:
                return self._diff_update_and_compare('publish', '', '')
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('publish', before, after)

    def diffparam_read_only(self):
        before = self.info['hostconfig']['readonlyrootfs']
        after = self.params['read_only']
        return self._diff_update_and_compare('read_only', before, after)

    def diffparam_restart_policy(self):
        before = self.info['hostconfig']['restartpolicy']['name']
        before_max_count = int(self.info['hostconfig']['restartpolicy'].get('maximumretrycount', 0))
        after = self.params['restart_policy'] or ""
        if ':' in after:
            after, after_max_count = after.rsplit(':', 1)
            after_max_count = int(after_max_count)
        else:
            after_max_count = 0
        before = "%s:%i" % (before, before_max_count)
        after = "%s:%i" % (after, after_max_count)
        return self._diff_update_and_compare('restart_policy', before, after)

    def diffparam_rm(self):
        before = self.info['hostconfig']['autoremove']
        after = self.params['rm']
        return self._diff_update_and_compare('rm', before, after)

    def diffparam_security_opt(self):
        unsorted_before = self.info['hostconfig']['securityopt']
        unsorted_after = self.params['security_opt']
        # In rootful containers with apparmor there is a profile, "container-default",
        # which is already added by default
        # Since SElinux labels are basically annotations, they are merged in a single list
        # element by podman so we need to split them in a (sorted) list if we want to compare it
        # to the list we provide to the module
        before = sorted(item for element in unsorted_before for item in element.split(',')
                        if 'apparmor=container-default' not in item)
        after = sorted(list(set(unsorted_after)))
        return self._diff_update_and_compare('security_opt', before, after)

    def diffparam_stop_signal(self):
        before = normalize_signal(self.info['config']['stopsignal'])
        after = normalize_signal(self.params['stop_signal'])
        return self._diff_update_and_compare('stop_signal', before, after)

    def diffparam_timezone(self):
        before = self.info['config'].get('timezone')
        after = self.params['timezone']
        return self._diff_update_and_compare('timezone', before, after)

    def diffparam_tmpfs(self):
        before = []
        if self.info['config'].get('createcommand'):
            cr_com = self.info['config']['createcommand']
            for i, v in enumerate(cr_com):
                if v == '--tmpfs':
                    before.append(cr_com[i + 1])
        after = []
        tmpfs = self.params.get('tmpfs')
        if tmpfs:
            for k, v in tmpfs.items():
                if v:
                    after.append('{0}:{1}'.format(self._clean_path(k), self._clean_path(v)))
                else:
                    after.append(self._clean_path(k))
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('tmpfs', before, after)

    def diffparam_tty(self):
        before = self.info['config']['tty']
        after = self.params['tty']
        return self._diff_update_and_compare('tty', before, after)

    def diffparam_user(self):
        before = self.info['config']['user']
        after = self.params['user']
        return self._diff_update_and_compare('user', before, after)

    def diffparam_ulimit(self):
        after = self.params['ulimit'] or []
        # In case of latest podman
        if 'createcommand' in self.info['config']:
            before = self._createcommand('--ulimit')
            before, after = sorted(before), sorted(after)
            return self._diff_update_and_compare('ulimit', before, after)
        if after:
            ulimits = self.info['hostconfig']['ulimits']
            before = {
                u['name'].replace('rlimit_', ''): "%s:%s" % (u['soft'], u['hard']) for u in ulimits}
            after = {i.split('=')[0]: i.split('=')[1]
                     for i in self.params['ulimit']}
            new_before = []
            new_after = []
            for u in list(after.keys()):
                # We don't support unlimited ulimits because it depends on platform
                if u in before and "-1" not in after[u]:
                    new_before.append([u, before[u]])
                    new_after.append([u, after[u]])
            return self._diff_update_and_compare('ulimit', new_before, new_after)
        return self._diff_update_and_compare('ulimit', '', '')

    def diffparam_uts(self):
        before = self.info['hostconfig']['utsmode']
        after = self.params['uts']
        if self.params['pod'] and not self.module_params['uts']:
            after = before
        return self._diff_update_and_compare('uts', before, after)

    def diffparam_volume(self):
        before = []
        if self.info['config'].get('createcommand'):
            cr_com = self.info['config']['createcommand']
            for i, v in enumerate(cr_com):
                if v == '--volume':
                    before = self._clean_path_in_mount_str(cr_com[i + 1])
        after = self.params.get('volume')
        if not after:
            after = []
        else:
            after = self._clean_path_in_mount_str(after)
        before, after = sorted(list(set(before))), sorted(list(set(after)))
        return self._diff_update_and_compare('volume', before, after)

    def diffparam_volumes_from(self):
        # Possibly volumesfrom is not in config
        before = self.info['hostconfig'].get('volumesfrom', []) or []
        after = self.params['volumes_from'] or []
        return self._diff_update_and_compare('volumes_from', before, after)

    def diffparam_workdir(self):
        before = self.info['config']['workingdir']
        after = self.params['workdir']
        return self._diff_update_and_compare('workdir', before, after)

    def is_different(self):
        diff_func_list = [func for func in dir(self)
                          if callable(getattr(self, func)) and func.startswith(
                              "diffparam")]
        fail_fast = not bool(self.module._diff)
        different = False
        for func_name in diff_func_list:
            dff_func = getattr(self, func_name)
            if dff_func():
                if fail_fast:
                    return True
                different = True
        # Check non idempotent parameters
        for p in self.non_idempotent:
            if self.module_params[p] is not None and self.module_params[p] not in [{}, [], '']:
                different = True
        return different


def ensure_image_exists(module, image, module_params):
    """If image is passed, ensure it exists, if not - pull it or fail.

    Arguments:
        module {obj} -- ansible module object
        image {str} -- name of image

    Returns:
        list -- list of image actions - if it pulled or nothing was done
    """
    image_actions = []
    module_exec = module_params['executable']
    is_rootfs = module_params['rootfs']

    if is_rootfs:
        if not os.path.exists(image) or not os.path.isdir(image):
            module.fail_json(msg="Image rootfs doesn't exist %s" % image)
        return image_actions
    if not image:
        return image_actions
    rc, out, err = module.run_command([module_exec, 'image', 'exists', image])
    if rc == 0:
        return image_actions
    rc, out, err = module.run_command([module_exec, 'image', 'pull', image])
    if rc != 0:
        module.fail_json(msg="Can't pull image %s" % image, stdout=out,
                         stderr=err)
    image_actions.append("pulled image %s" % image)
    return image_actions


class PodmanContainer:
    """Perform container tasks.

    Manages podman container, inspects it and checks its current state
    """

    def __init__(self, module, name, module_params):
        """Initialize PodmanContainer class.

        Arguments:
            module {obj} -- ansible module object
            name {str} -- name of container
        """

        self.module = module
        self.module_params = module_params
        self.name = name
        self.stdout, self.stderr = '', ''
        self.info = self.get_info()
        self.version = self._get_podman_version()
        self.diff = {}
        self.actions = []

    @property
    def exists(self):
        """Check if container exists."""
        return bool(self.info != {})

    @property
    def different(self):
        """Check if container is different."""
        diffcheck = PodmanContainerDiff(
            self.module,
            self.module_params,
            self.info,
            self.get_image_info(),
            self.version)
        is_different = diffcheck.is_different()
        diffs = diffcheck.diff
        if self.module._diff and is_different and diffs['before'] and diffs['after']:
            self.diff['before'] = "\n".join(
                ["%s - %s" % (k, v) for k, v in sorted(
                    diffs['before'].items())]) + "\n"
            self.diff['after'] = "\n".join(
                ["%s - %s" % (k, v) for k, v in sorted(
                    diffs['after'].items())]) + "\n"
        return is_different

    @property
    def running(self):
        """Return True if container is running now."""
        return self.exists and self.info['State']['Running']

    @property
    def stopped(self):
        """Return True if container exists and is not running now."""
        return self.exists and not self.info['State']['Running']

    def get_info(self):
        """Inspect container and gather info about it."""
        # pylint: disable=unused-variable
        rc, out, err = self.module.run_command(
            [self.module_params['executable'], b'container', b'inspect', self.name])
        return json.loads(out)[0] if rc == 0 else {}

    def get_image_info(self):
        """Inspect container image and gather info about it."""
        # pylint: disable=unused-variable
        is_rootfs = self.module_params['rootfs']
        if is_rootfs:
            return {'Id': self.module_params['image']}
        rc, out, err = self.module.run_command(
            [self.module_params['executable'], b'image', b'inspect', self.module_params['image']])
        return json.loads(out)[0] if rc == 0 else {}

    def _get_podman_version(self):
        # pylint: disable=unused-variable
        rc, out, err = self.module.run_command(
            [self.module_params['executable'], b'--version'])
        if rc != 0 or not out or "version" not in out:
            self.module.fail_json(msg="%s run failed!" %
                                  self.module_params['executable'])
        return out.split("version")[1].strip()

    def _perform_action(self, action):
        """Perform action with container.

        Arguments:
            action {str} -- action to perform - start, create, stop, run,
                            delete, restart
        """
        b_command = PodmanModuleParams(action,
                                       self.module_params,
                                       self.version,
                                       self.module,
                                       ).construct_command_from_params()
        full_cmd = " ".join([self.module_params['executable']]
                            + [to_native(i) for i in b_command])
        self.actions.append(full_cmd)
        if self.module.check_mode:
            self.module.log(
                "PODMAN-CONTAINER-DEBUG (check_mode): %s" % full_cmd)
        else:
            rc, out, err = self.module.run_command(
                [self.module_params['executable'], b'container'] + b_command,
                expand_user_and_vars=False)
            self.module.log("PODMAN-CONTAINER-DEBUG: %s" % full_cmd)
            if self.module_params['debug']:
                self.module.log("PODMAN-CONTAINER-DEBUG STDOUT: %s" % out)
                self.module.log("PODMAN-CONTAINER-DEBUG STDERR: %s" % err)
                self.module.log("PODMAN-CONTAINER-DEBUG RC: %s" % rc)
            self.stdout = out
            self.stderr = err
            if rc != 0:
                self.module.fail_json(
                    msg="Container %s exited with code %s when %sed" % (self.name, rc, action),
                    stdout=out, stderr=err)

    def run(self):
        """Run the container."""
        self._perform_action('run')

    def delete(self):
        """Delete the container."""
        self._perform_action('delete')

    def stop(self):
        """Stop the container."""
        self._perform_action('stop')

    def start(self):
        """Start the container."""
        self._perform_action('start')

    def restart(self):
        """Restart the container."""
        self._perform_action('restart')

    def create(self):
        """Create the container."""
        self._perform_action('create')

    def recreate(self):
        """Recreate the container."""
        if self.running:
            self.stop()
        if not self.info['HostConfig']['AutoRemove']:
            self.delete()
        self.create()

    def recreate_run(self):
        """Recreate and run the container."""
        if self.running:
            self.stop()
        if not self.info['HostConfig']['AutoRemove']:
            self.delete()
        self.run()


class PodmanManager:
    """Module manager class.

    Defines according to parameters what actions should be applied to container
    """

    def __init__(self, module, params):
        """Initialize PodmanManager class.

        Arguments:
            module {obj} -- ansible module object
        """

        self.module = module
        self.results = {
            'changed': False,
            'actions': [],
            'container': {},
        }
        self.module_params = params
        self.name = self.module_params['name']
        self.executable = \
            self.module.get_bin_path(self.module_params['executable'],
                                     required=True)
        self.image = self.module_params['image']
        image_actions = ensure_image_exists(
            self.module, self.image, self.module_params)
        self.results['actions'] += image_actions
        self.state = self.module_params['state']
        self.restart = self.module_params['force_restart']
        self.recreate = self.module_params['recreate']

        if self.module_params['generate_systemd'].get('new'):
            self.module_params['rm'] = True

        self.container = PodmanContainer(
            self.module, self.name, self.module_params)

    def update_container_result(self, changed=True):
        """Inspect the current container, update results with last info, exit.

        Keyword Arguments:
            changed {bool} -- whether any action was performed
                              (default: {True})
        """
        facts = self.container.get_info() if changed else self.container.info
        out, err = self.container.stdout, self.container.stderr
        self.results.update({'changed': changed, 'container': facts,
                             'podman_actions': self.container.actions},
                            stdout=out, stderr=err)
        if self.container.diff:
            self.results.update({'diff': self.container.diff})
        if self.module.params['debug'] or self.module_params['debug']:
            self.results.update({'podman_version': self.container.version})
        sysd = generate_systemd(self.module,
                                self.module_params,
                                self.name,
                                self.container.version)
        self.results['changed'] = changed or sysd['changed']
        self.results.update(
            {'podman_systemd': sysd['systemd']})
        if sysd['diff']:
            if 'diff' not in self.results:
                self.results.update({'diff': sysd['diff']})
            else:
                self.results['diff']['before'] += sysd['diff']['before']
                self.results['diff']['after'] += sysd['diff']['after']

    def make_started(self):
        """Run actions if desired state is 'started'."""
        if not self.image:
            if not self.container.exists:
                self.module.fail_json(msg='Cannot start container when image'
                                          ' is not specified!')
            if self.restart:
                self.container.restart()
                self.results['actions'].append('restarted %s' %
                                               self.container.name)
            else:
                self.container.start()
                self.results['actions'].append('started %s' %
                                               self.container.name)
            self.update_container_result()
            return
        if self.container.exists and self.restart:
            if self.container.running:
                self.container.restart()
                self.results['actions'].append('restarted %s' %
                                               self.container.name)
            else:
                self.container.start()
                self.results['actions'].append('started %s' %
                                               self.container.name)
            self.update_container_result()
            return
        if self.container.running and \
                (self.container.different or self.recreate):
            self.container.recreate_run()
            self.results['actions'].append('recreated %s' %
                                           self.container.name)
            self.update_container_result()
            return
        elif self.container.running and not self.container.different:
            if self.restart:
                self.container.restart()
                self.results['actions'].append('restarted %s' %
                                               self.container.name)
                self.update_container_result()
                return
            self.update_container_result(changed=False)
            return
        elif not self.container.exists:
            self.container.run()
            self.results['actions'].append('started %s' % self.container.name)
            self.update_container_result()
            return
        elif self.container.stopped and \
                (self.container.different or self.recreate):
            self.container.recreate_run()
            self.results['actions'].append('recreated %s' %
                                           self.container.name)
            self.update_container_result()
            return
        elif self.container.stopped and not self.container.different:
            self.container.start()
            self.results['actions'].append('started %s' % self.container.name)
            self.update_container_result()
            return

    def make_created(self):
        """Run actions if desired state is 'created'."""
        if not self.container.exists and not self.image:
            self.module.fail_json(msg='Cannot create container when image'
                                      ' is not specified!')
        if not self.container.exists:
            self.container.create()
            self.results['actions'].append('created %s' % self.container.name)
            self.update_container_result()
            return
        else:
            if (self.container.different or self.recreate):
                self.container.recreate()
                self.results['actions'].append('recreated %s' %
                                               self.container.name)
                if self.container.running:
                    self.container.start()
                    self.results['actions'].append('started %s' %
                                                   self.container.name)
                self.update_container_result()
                return
            elif self.restart:
                if self.container.running:
                    self.container.restart()
                    self.results['actions'].append('restarted %s' %
                                                   self.container.name)
                else:
                    self.container.start()
                    self.results['actions'].append('started %s' %
                                                   self.container.name)
                self.update_container_result()
                return
            self.update_container_result(changed=False)
            return

    def make_stopped(self):
        """Run actions if desired state is 'stopped'."""
        if not self.container.exists and not self.image:
            self.module.fail_json(msg='Cannot create container when image'
                                      ' is not specified!')
        if not self.container.exists:
            self.container.create()
            self.results['actions'].append('created %s' % self.container.name)
            self.update_container_result()
            return
        if self.container.stopped:
            self.update_container_result(changed=False)
            return
        elif self.container.running:
            self.container.stop()
            self.results['actions'].append('stopped %s' % self.container.name)
            self.update_container_result()
            return

    def make_absent(self):
        """Run actions if desired state is 'absent'."""
        if not self.container.exists:
            self.results.update({'changed': False})
        elif self.container.exists:
            delete_systemd(self.module,
                           self.module_params,
                           self.name,
                           self.container.version)
            self.container.delete()
            self.results['actions'].append('deleted %s' % self.container.name)
            self.results.update({'changed': True})
        self.results.update({'container': {},
                             'podman_actions': self.container.actions})

    def execute(self):
        """Execute the desired action according to map of actions & states."""
        states_map = {
            'present': self.make_created,
            'started': self.make_started,
            'absent': self.make_absent,
            'stopped': self.make_stopped,
            'created': self.make_created,
        }
        process_action = states_map[self.state]
        process_action()
        return self.results
