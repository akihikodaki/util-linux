diff --git a/sys-utils/swapon.c b/sys-utils/swapon.c
index 914e69a..97acf1e 100644
--- a/sys-utils/swapon.c
+++ b/sys-utils/swapon.c
@@ -99,22 +99,33 @@ struct colinfo infos[] = {
 	[COL_LABEL]    = { "LABEL",	0.20, 0, N_("swap label")},
 };
 
-/* control struct */
-struct swapon_ctl {
-	const char *device;		/* device or file to be turned on */
-	const char *options;		/* fstab-compatible option string */
+
+/* swap area properties */
+struct swap_prop {
+	int discard;			/* discard policy */
+	int priority;			/* non-prioritized swap by default */
+	int no_fail;			/* skip device if not exist */
+};
+
+/* device description */
+struct swap_device {
+	const char *path;		/* device or file to be turned on */
 	const char *label;		/* swap label */
 	const char *uuid;		/* unique identifier */
-	int discard;			/* discard policy */
+	unsigned int pagesize;
+};
+
+/* control struct */
+struct swapon_ctl {
 	int columns[ARRAY_SIZE(infos) * 2];	/* --show columns */
-	int ncolumns;			/* number of columns */
-	int priority;			/* non-prioritized swap by default */
-	unsigned int pagesize;		/* swap page size */
+	int ncolumns;				/* number of columns */
+
+	struct swap_prop props;		/* global settings for all devices */
+
 	unsigned int
 		all:1,			/* turn on all swap devices */
 		bytes:1,		/* display --show in bytes */
 		fix_page_size:1,	/* reinitialize page size */
-		no_fail:1,		/* skip devices that do not exist */
 		no_heading:1,		/* toggle --show headers */
 		raw:1,			/* toggle --show alignment */
 		show:1,			/* display --show information */
@@ -288,14 +299,17 @@ static int show_table(struct swapon_ctl *ctl)
 }
 
 /* calls mkswap */
-static int swap_reinitialize(struct swapon_ctl *ctl)
+static int swap_reinitialize(struct swap_device *dev)
 {
 	pid_t pid;
 	int status, ret;
 	char const *cmd[7];
 	int idx=0;
 
-	warnx(_("%s: reinitializing the swap."), ctl->device);
+	assert(dev);
+	assert(dev->path);
+
+	warnx(_("%s: reinitializing the swap."), dev->path);
 
 	switch ((pid=fork())) {
 	case -1: /* fork error */
@@ -312,15 +326,15 @@ static int swap_reinitialize(struct swapon_ctl *ctl)
 		}
 
 		cmd[idx++] = "mkswap";
-		if (ctl->label) {
+		if (dev->label) {
 			cmd[idx++] = "-L";
-			cmd[idx++] = ctl->label;
+			cmd[idx++] = dev->label;
 		}
-		if (ctl->uuid) {
+		if (dev->uuid) {
 			cmd[idx++] = "-U";
-			cmd[idx++] = ctl->uuid;
+			cmd[idx++] = dev->uuid;
 		}
-		cmd[idx++] = ctl->device;
+		cmd[idx++] = dev->path;
 		cmd[idx++] = NULL;
 		execvp(cmd[0], (char * const *) cmd);
 		err(EXIT_FAILURE, _("failed to execute %s"), cmd[0]);
@@ -343,31 +357,36 @@ static int swap_reinitialize(struct swapon_ctl *ctl)
 	return -1; /* error */
 }
 
-static int swap_rewrite_signature(const struct swapon_ctl *ctl)
+/* Replaces unwanted SWSUSPEND signature with swap signature */
+static int swap_rewrite_signature(const struct swap_device *dev)
 {
 	int fd, rc = -1;
 
-	fd = open(ctl->device, O_WRONLY);
+	assert(dev);
+	assert(dev->path);
+	assert(dev->pagesize);
+
+	fd = open(dev->path, O_WRONLY);
 	if (fd == -1) {
-		warn(_("cannot open %s"), ctl->device);
+		warn(_("cannot open %s"), dev->path);
 		return -1;
 	}
 
-	if (lseek(fd, ctl->pagesize - SWAP_SIGNATURE_SZ, SEEK_SET) < 0) {
-		warn(_("%s: lseek failed"), ctl->device);
+	if (lseek(fd, dev->pagesize - SWAP_SIGNATURE_SZ, SEEK_SET) < 0) {
+		warn(_("%s: lseek failed"), dev->path);
 		goto err;
 	}
 
 	if (write(fd, (void *) SWAP_SIGNATURE,
 			SWAP_SIGNATURE_SZ) != SWAP_SIGNATURE_SZ) {
-		warn(_("%s: write signature failed"), ctl->device);
+		warn(_("%s: write signature failed"), dev->path);
 		goto err;
 	}
 
 	rc  = 0;
 err:
 	if (close_fd(fd) != 0) {
-		warn(_("write failed: %s"), ctl->device);
+		warn(_("write failed: %s"), dev->path);
 		rc = -1;
 	}
 	return rc;
@@ -375,6 +394,9 @@ err:
 
 static int swap_detect_signature(const char *buf, int *sig)
 {
+	assert(buf);
+	assert(sig);
+
 	if (memcmp(buf, SWAP_SIGNATURE, SWAP_SIGNATURE_SZ) == 0)
 		*sig = SIG_SWAPSPACE;
 
@@ -390,13 +412,16 @@ static int swap_detect_signature(const char *buf, int *sig)
 	return 1;
 }
 
-static char *swap_get_header(struct swapon_ctl *ctl, int fd, int *sig)
+static char *swap_get_header(int fd, int *sig, unsigned int *pagesize)
 {
 	char *buf;
 	ssize_t datasz;
 	unsigned int page;
 
-	ctl->pagesize = 0;
+	assert(sig);
+	assert(pagesize);
+
+	*pagesize = 0;
 	*sig = 0;
 
 	buf = xmalloc(MAX_PAGESIZE);
@@ -415,12 +440,12 @@ static char *swap_get_header(struct swapon_ctl *ctl, int fd, int *sig)
 		if (datasz < 0 || (size_t) datasz < (page - SWAP_SIGNATURE_SZ))
 			break;
 		if (swap_detect_signature(buf + page - SWAP_SIGNATURE_SZ, sig)) {
-			ctl->pagesize = page;
+			*pagesize = page;
 			break;
 		}
 	}
 
-	if (ctl->pagesize)
+	if (*pagesize)
 		return buf;
 err:
 	free(buf);
@@ -428,37 +453,34 @@ err:
 }
 
 /* returns real size of swap space */
-static unsigned long long swap_get_size(const struct swapon_ctl *ctl, const char *hdr)
+static unsigned long long swap_get_size(const struct swap_device *dev,
+					const char *hdr)
 {
 	unsigned int last_page = 0;
 	const unsigned int swap_version = SWAP_VERSION;
-	int flip = 0;
 	struct swap_header_v1_2 *s;
 
+	assert(dev);
+	assert(dev->pagesize > 0);
+
 	s = (struct swap_header_v1_2 *) hdr;
-	if (s->version == swap_version) {
+
+	if (s->version == swap_version)
 		last_page = s->last_page;
-	} else if (swab32(s->version) == swap_version) {
-		flip = 1;
+	else if (swab32(s->version) == swap_version)
 		last_page = swab32(s->last_page);
-	}
-	if (ctl->verbose)
-		warnx(_("%s: found swap signature: version %ud, "
-			"page-size %d, %s byte order"),
-			ctl->device,
-			swap_version,
-			ctl->pagesize / 1024,
-			flip ? _("different") : _("same"));
-
-	return ((unsigned long long) last_page + 1) * ctl->pagesize;
+
+	return ((unsigned long long) last_page + 1) * dev->pagesize;
 }
 
-static void swap_get_info(struct swapon_ctl *ctl, const char *hdr)
+static void swap_get_info(struct swap_device *dev, const char *hdr)
 {
 	struct swap_header_v1_2 *s = (struct swap_header_v1_2 *) hdr;
 
+	assert(dev);
+
 	if (s && *s->volume_name)
-		ctl->label = xstrdup(s->volume_name);
+		dev->label = xstrdup(s->volume_name);
 
 	if (s && *s->uuid) {
 		const unsigned char *u = s->uuid;
@@ -471,11 +493,11 @@ static void swap_get_info(struct swapon_ctl *ctl, const char *hdr)
 			u[0], u[1], u[2], u[3],
 			u[4], u[5], u[6], u[7],
 			u[8], u[9], u[10], u[11], u[12], u[13], u[14], u[15]);
-		ctl->uuid = xstrdup(str);
+		dev->uuid = xstrdup(str);
 	}
 }
 
-static int swapon_checks(struct swapon_ctl *ctl)
+static int swapon_checks(const struct swapon_ctl *ctl, struct swap_device *dev)
 {
 	struct stat st;
 	int fd = -1, sig;
@@ -483,77 +505,88 @@ static int swapon_checks(struct swapon_ctl *ctl)
 	unsigned long long devsize = 0;
 	int permMask;
 
-	fd = open(ctl->device, O_RDONLY);
+	assert(ctl);
+	assert(dev);
+	assert(dev->path);
+
+	fd = open(dev->path, O_RDONLY);
 	if (fd == -1) {
-		warn(_("cannot open %s"), ctl->device);
+		warn(_("cannot open %s"), dev->path);
 		goto err;
 	}
 
 	if (fstat(fd, &st) < 0) {
-		warn(_("stat of %s failed"), ctl->device);
+		warn(_("stat of %s failed"), dev->path);
 		goto err;
 	}
 
 	permMask = S_ISBLK(st.st_mode) ? 07007 : 07077;
 	if ((st.st_mode & permMask) != 0)
 		warnx(_("%s: insecure permissions %04o, %04o suggested."),
-				ctl->device, st.st_mode & 07777,
+				dev->path, st.st_mode & 07777,
 				~permMask & 0666);
 
 	if (S_ISREG(st.st_mode) && st.st_uid != 0)
 		warnx(_("%s: insecure file owner %d, 0 (root) suggested."),
-				ctl->device, st.st_uid);
+				dev->path, st.st_uid);
 
 	/* test for holes by LBT */
 	if (S_ISREG(st.st_mode)) {
 		if (st.st_blocks * 512 < st.st_size) {
 			warnx(_("%s: skipping - it appears to have holes."),
-				ctl->device);
+				dev->path);
 			goto err;
 		}
 		devsize = st.st_size;
 	}
 
 	if (S_ISBLK(st.st_mode) && blkdev_get_size(fd, &devsize)) {
-		warnx(_("%s: get size failed"), ctl->device);
+		warnx(_("%s: get size failed"), dev->path);
 		goto err;
 	}
 
-	hdr = swap_get_header(ctl, fd, &sig);
+	hdr = swap_get_header(fd, &sig, &dev->pagesize);
 	if (!hdr) {
-		warnx(_("%s: read swap header failed"), ctl->device);
+		warnx(_("%s: read swap header failed"), dev->path);
 		goto err;
 	}
 
-	if (sig == SIG_SWAPSPACE && ctl->pagesize) {
-		unsigned long long swapsize =
-				swap_get_size(ctl, hdr);
+	if (ctl->verbose)
+		warnx(_("%s: found signature [pagesize=%d, signature=%s]"),
+			dev->path,
+			dev->pagesize,
+			sig == SIG_SWAPSPACE ? "swap" :
+			sig == SIG_SWSUSPEND ? "suspend" : "unknown");
+
+	if (sig == SIG_SWAPSPACE && dev->pagesize) {
+		unsigned long long swapsize = swap_get_size(dev, hdr);
 		int syspg = getpagesize();
 
 		if (ctl->verbose)
 			warnx(_("%s: pagesize=%d, swapsize=%llu, devsize=%llu"),
-				ctl->device, ctl->pagesize, swapsize, devsize);
+				dev->path, dev->pagesize, swapsize, devsize);
 
 		if (swapsize > devsize) {
 			if (ctl->verbose)
 				warnx(_("%s: last_page 0x%08llx is larger"
 					" than actual size of swapspace"),
-					ctl->device, swapsize);
-		} else if (syspg < 0 || (unsigned int) syspg != ctl->pagesize) {
+					dev->path, swapsize);
+
+		} else if (syspg < 0 || (unsigned int) syspg != dev->pagesize) {
 			if (ctl->fix_page_size) {
 				int rc;
 
-				swap_get_info(ctl, hdr);
+				swap_get_info(dev, hdr);
 
 				warnx(_("%s: swap format pagesize does not match."),
-					ctl->device);
-				rc = swap_reinitialize(ctl);
+					dev->path);
+				rc = swap_reinitialize(dev);
 				if (rc < 0)
 					goto err;
 			} else
 				warnx(_("%s: swap format pagesize does not match. "
 					"(Use --fixpgsz to reinitialize it.)"),
-					ctl->device);
+					dev->path);
 		}
 	} else if (sig == SIG_SWSUSPEND) {
 		/* We have to reinitialize swap with old (=useless) software suspend
@@ -562,8 +595,8 @@ static int swapon_checks(struct swapon_ctl *ctl)
 		 */
 		warnx(_("%s: software suspend data detected. "
 				"Rewriting the swap signature."),
-			ctl->device);
-		if (swap_rewrite_signature(ctl) < 0)
+			dev->path);
+		if (swap_rewrite_signature(dev) < 0)
 			goto err;
 	}
 
@@ -577,33 +610,38 @@ err:
 	return -1;
 }
 
-static int do_swapon(struct swapon_ctl *ctl, const char *spec, int canonic)
+static int do_swapon(const struct swapon_ctl *ctl,
+		     const struct swap_prop *prop,
+		     const char *spec,
+		     int canonic)
 {
+	struct swap_device dev = { .path = NULL };
 	int status;
 	int flags = 0;
+	int priority;
 
-	/* all initilized by do_swapon() */
-	ctl->device = ctl->label = ctl->uuid = NULL;
-
-	if (ctl->verbose)
-		printf(_("swapon %s\n"), ctl->device);
+	assert(ctl);
+	assert(prop);
 
 	if (!canonic) {
-		ctl->device = mnt_resolve_spec(spec, mntcache);
-		if (!ctl->device)
+		dev.path = mnt_resolve_spec(spec, mntcache);
+		if (!dev.path)
 			return cannot_find(spec);
 	} else
-		ctl->device = spec;
+		dev.path = spec;
 
-	if (swapon_checks(ctl))
+	priority = prop->priority;
+
+	if (swapon_checks(ctl, &dev))
 		return -1;
 
 #ifdef SWAP_FLAG_PREFER
-	if (ctl->priority >= 0) {
-		if (ctl->priority > SWAP_FLAG_PRIO_MASK)
-			ctl->priority = SWAP_FLAG_PRIO_MASK;
+	if (priority >= 0) {
+		if (priority > SWAP_FLAG_PRIO_MASK)
+			priority = SWAP_FLAG_PRIO_MASK;
+
 		flags = SWAP_FLAG_PREFER
-			| ((ctl->priority & SWAP_FLAG_PRIO_MASK)
+			| ((priority & SWAP_FLAG_PRIO_MASK)
 			   << SWAP_FLAG_PRIO_SHIFT);
 	}
 #endif
@@ -611,22 +649,25 @@ static int do_swapon(struct swapon_ctl *ctl, const char *spec, int canonic)
 	 * Validate the discard flags passed and set them
 	 * accordingly before calling sys_swapon.
 	 */
-	if (ctl->discard && !(ctl->discard & ~SWAP_FLAGS_DISCARD_VALID)) {
+	if (prop->discard && !(prop->discard & ~SWAP_FLAGS_DISCARD_VALID)) {
 		/*
 		 * If we get here with both discard policy flags set,
 		 * we just need to tell the kernel to enable discards
 		 * and it will do correctly, just as we expect.
 		 */
-		if ((ctl->discard & SWAP_FLAG_DISCARD_ONCE) &&
-		    (ctl->discard & SWAP_FLAG_DISCARD_PAGES))
+		if ((prop->discard & SWAP_FLAG_DISCARD_ONCE) &&
+		    (prop->discard & SWAP_FLAG_DISCARD_PAGES))
 			flags |= SWAP_FLAG_DISCARD;
 		else
-			flags |= ctl->discard;
+			flags |= prop->discard;
 	}
 
-	status = swapon(ctl->device, flags);
+	if (ctl->verbose)
+		printf(_("swapon %s\n"), dev.path);
+
+	status = swapon(dev.path, flags);
 	if (status < 0)
-		warn(_("%s: swapon failed"), ctl->device);
+		warn(_("%s: swapon failed"), dev.path);
 
 	return status;
 }
@@ -634,45 +675,43 @@ static int do_swapon(struct swapon_ctl *ctl, const char *spec, int canonic)
 static int swapon_by_label(struct swapon_ctl *ctl, const char *label)
 {
 	char *device = mnt_resolve_tag("LABEL", label, mntcache);
-	return device ? do_swapon(ctl, device, TRUE) :  cannot_find(label);
+	return device ? do_swapon(ctl, &ctl->props, device, TRUE) :  cannot_find(label);
 }
 
 static int swapon_by_uuid(struct swapon_ctl *ctl, const char *uuid)
 {
 	char *device = mnt_resolve_tag("UUID", uuid, mntcache);
-	return device ? do_swapon(ctl, device, TRUE) : cannot_find(uuid);
+	return device ? do_swapon(ctl, &ctl->props, device, TRUE) : cannot_find(uuid);
 }
 
 /* -o <options> or fstab */
-static int parse_options(struct swapon_ctl *ctl)
+static int parse_options(struct swap_prop *props, const char *options)
 {
 	char *arg = NULL;
 
-	assert(ctl->options);
-	assert(ctl->priority);
-	assert(ctl->discard);
-	assert(ctl->no_fail);
+	assert(props);
+	assert(options);
 
-	if (mnt_optstr_get_option(ctl->options, "nofail", NULL, 0) == 0)
-		ctl->no_fail = 1;
+	if (mnt_optstr_get_option(options, "nofail", NULL, 0) == 0)
+		props->no_fail = 1;
 
-	if (mnt_optstr_get_option(ctl->options, "discard", &arg, NULL) == 0) {
-		ctl->discard |= SWAP_FLAG_DISCARD;
+	if (mnt_optstr_get_option(options, "discard", &arg, NULL) == 0) {
+		props->discard |= SWAP_FLAG_DISCARD;
 
 		if (arg) {
 			/* only single-time discards are wanted */
 			if (strcmp(arg, "once") == 0)
-				ctl->discard |= SWAP_FLAG_DISCARD_ONCE;
+				props->discard |= SWAP_FLAG_DISCARD_ONCE;
 
 			/* do discard for every released swap page */
 			if (strcmp(arg, "pages") == 0)
-				ctl->discard |= SWAP_FLAG_DISCARD_PAGES;
-			}
+				props->discard |= SWAP_FLAG_DISCARD_PAGES;
+		}
 	}
 
 	arg = NULL;
-	if (mnt_optstr_get_option(ctl->options, "pri", &arg, NULL) == 0 && arg)
-		ctl->priority = atoi(arg);
+	if (mnt_optstr_get_option(options, "pri", &arg, NULL) == 0 && arg)
+		props->priority = atoi(arg);
 
 	return 0;
 }
@@ -696,24 +735,44 @@ static int swapon_all(struct swapon_ctl *ctl)
 		/* defaults */
 		const char *opts;
 		const char *device;
+		struct swap_prop prop;		/* per device setting */
 
-		if (mnt_fs_get_option(fs, "noauto", NULL, NULL) == 0)
+		if (mnt_fs_get_option(fs, "noauto", NULL, NULL) == 0) {
+			if (ctl->verbose)
+				warnx(_("%s: noauto option -- ignored"), mnt_fs_get_source(fs));
 			continue;
+		}
+
+		/* default setting */
+		prop = ctl->props;
 
+		/* overwrite default by setting from fstab */
 		opts = mnt_fs_get_options(fs);
 		if (opts)
-			parse_options(ctl);
+			parse_options(&prop, opts);
 
+		/* convert LABEL=, UUID= etc. from fstab to device name */
 		device = mnt_resolve_spec(mnt_fs_get_source(fs), mntcache);
 		if (!device) {
-			if (!ctl->no_fail)
+			if (!prop.no_fail)
 				status |= cannot_find(mnt_fs_get_source(fs));
 			continue;
 		}
 
-		if (!is_active_swap(device) &&
-		    (!ctl->no_fail || !access(device, R_OK)))
-			status |= do_swapon(ctl, device, TRUE);
+		if (is_active_swap(device)) {
+			if (ctl->verbose)
+				warnx(_("%s: already active -- ignored"), device);
+			continue;
+		}
+
+		if (prop.no_fail && access(device, R_OK) != 0) {
+			if (ctl->verbose)
+				warnx(_("%s: unaccessible -- ignored"), device);
+			continue;
+		}
+
+		/* swapon */
+		status |= do_swapon(ctl, &prop, device, TRUE);
 	}
 
 	mnt_free_iter(itr);
@@ -775,6 +834,7 @@ int main(int argc, char *argv[])
 {
 	int status = 0, c;
 	size_t i;
+	char *options = NULL;
 
 	enum {
 		BYTES_OPTION = CHAR_MAX + 1,
@@ -810,13 +870,16 @@ int main(int argc, char *argv[])
 	};
 	int excl_st[ARRAY_SIZE(excl)] = UL_EXCL_STATUS_INIT;
 
-	struct swapon_ctl ctl = { .priority = -1 };
+	struct swapon_ctl ctl;
 
 	setlocale(LC_ALL, "");
 	bindtextdomain(PACKAGE, LOCALEDIR);
 	textdomain(PACKAGE);
 	atexit(close_stdout);
 
+	memset(&ctl, 0, sizeof(struct swapon_ctl));
+	ctl.props.priority = -1;
+
 	mnt_init_debug(0);
 	mntcache = mnt_new_cache();
 
@@ -833,10 +896,10 @@ int main(int argc, char *argv[])
 			usage(stdout);
 			break;
 		case 'o':
-			ctl.options = optarg;
+			options = optarg;
 			break;
 		case 'p':		/* priority */
-			ctl.priority = strtos16_or_err(optarg,
+			ctl.props.priority = strtos16_or_err(optarg,
 					   _("failed to parse priority"));
 			break;
 		case 'L':
@@ -846,21 +909,21 @@ int main(int argc, char *argv[])
 			add_uuid(optarg);
 			break;
 		case 'd':
-			ctl.discard |= SWAP_FLAG_DISCARD;
+			ctl.props.discard |= SWAP_FLAG_DISCARD;
 			if (optarg) {
 				if (*optarg == '=')
 					optarg++;
 
 				if (strcmp(optarg, "once") == 0)
-					ctl.discard |= SWAP_FLAG_DISCARD_ONCE;
+					ctl.props.discard |= SWAP_FLAG_DISCARD_ONCE;
 				else if (strcmp(optarg, "pages") == 0)
-					ctl.discard |= SWAP_FLAG_DISCARD_PAGES;
+					ctl.props.discard |= SWAP_FLAG_DISCARD_PAGES;
 				else
 					errx(EXIT_FAILURE, _("unsupported discard policy: %s"), optarg);
 			}
 			break;
 		case 'e':               /* ifexists */
-			ctl.no_fail = 1;
+			ctl.props.no_fail = 1;
 			break;
 		case 'f':
 			ctl.fix_page_size = 1;
@@ -916,14 +979,14 @@ int main(int argc, char *argv[])
 		return status;
 	}
 
-	if (ctl.no_fail && !ctl.all)
+	if (ctl.props.no_fail && !ctl.all)
 		usage(stderr);
 
 	if (ctl.all)
 		status |= swapon_all(&ctl);
 
-	if (ctl.options)
-		parse_options(&ctl);
+	if (options)
+		parse_options(&ctl.props, options);
 
 	for (i = 0; i < numof_labels(); i++)
 		status |= swapon_by_label(&ctl, get_label(i));
@@ -932,7 +995,7 @@ int main(int argc, char *argv[])
 		status |= swapon_by_uuid(&ctl, get_uuid(i));
 
 	while (*argv != NULL)
-		status |= do_swapon(&ctl, *argv++, FALSE);
+		status |= do_swapon(&ctl, &ctl.props, *argv++, FALSE);
 
 	free_tables();
 	mnt_unref_cache(mntcache);
