'''

EC2 instance types for current generation. This script does not optimize
older generations. Following matrix is replicated from:
   https://aws.amazon.com/ec2/instance-types/#instance-type-matrix
XXX: Is it worth to optimize this table?
This file is not pep8 compliant intentionally.
'''
general_purpose = (
("Instance Type", "vCPU", "Mem (GiB)", "Instance Storage (GiB)", "Networking Performance",  "CPU", "Clock Speed (GHz)", "Intel AVX", "Intel AVX2", "Intel Turbo", "EBS OPT", "Enhanced Networking"),
("t2.nano",      1,  0.5, "EBS-Only",         "Low",             "Intel Xeon family",       "up to 3.3", "Yes", "-",   "Yes",  "-",  "-"),
("t2.micro",     1,  1,   "EBS-Only",         "Low to Moderate", "Intel Xeon family",       "Up to 3.3", "Yes", "-",   "Yes",  "-",  "-"),
("t2.small",     1,  2,   "EBS-Only",         "Low to Moderate", "Intel Xeon family",       "Up to 3.3", "Yes", "-",   "Yes",  "-",  "-"),
("t2.medium",    2,  4,   "EBS-Only",         "Low to Moderate", "Intel Xeon family",       "Up to 3.3", "Yes", "-",   "Yes",  "-",  "-"),
("t2.large",     2,  8,   "EBS-Only",         "Low to Moderate", "Intel Xeon family",       "Up to 3.0", "Yes", "-",   "Yes",  "-",  "-"),
("t2.xlarge",    4,  16,  "EBS-Only",         "Moderate",        "Intel Xeon family",       "Up to 3.0", "Yes", "-",   "Yes",  "-",  "-"),
("t2.2xlarge",   8,  32,  "EBS-Only",         "Moderate",        "Intel Xeon family",       "Up to 3.0", "Yes", "-",   "Yes",  "-",  "-"),
("m5.large",     2,  8,   "EBS-Only",         "High",            "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5.xlarge",    4,  16,  "EBS-Only",         "High",            "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5.2xlarge",   8,  32,  "EBS-Only",         "High",            "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5.4xlarge",   16, 64,  "EBS-Only",         "High",            "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5.12xlarge",  48, 192, "EBS-Only",         "10 Gigabit",      "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5.24xlarge",  96, 384, "EBS-Only",         "25 Gigabit",      "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5d.large",    2,  8,   "1 x 75 NVMe SSD",  "High",            "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5d.xlarge",   4,  16,  "1 x 150 NVMe SSD", "High",            "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5d.2xlarge",  8,  32,  "1 x 300 NVMe SSD", "High",            "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5d.4xlarge",  16, 64,  "2 x 300 NVMe SSD", "High",            "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5d.12xlarge", 48, 192, "2 x 900 NVMe SSD", "10 Gigabit",      "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m5d.24xlarge", 96, 384, "4 x 900 NVMe SSD", "25 Gigabit",      "Intel Xeon Platinum",     "2.5",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m4.large",     2,  8,   "EBS-Only",         "Moderate",        "Intel Xeon E5-2676 v3**", "2.4",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m4.xlarge",    4,  16,  "EBS-Only",         "High",            "Intel Xeon E5-2676 v3**", "2.4",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m4.2xlarge",   8,  32,  "EBS-Only",         "High",            "Intel Xeon E5-2676 v3**", "2.4",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m4.4xlarge",   16, 64,  "EBS-Only",         "High",            "Intel Xeon E5-2676 v3**", "2.4",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m4.10xlarge",  40, 160, "EBS-Only",         "10 Gigabit",      "Intel Xeon E5-2676 v3",   "2.4",       "Yes", "Yes", "Yes", "Yes", "Yes"),
("m4.16xlarge",  64, 256, "EBS-Only",         "25 Gigabit",      "Intel Xeon E5-2686 v4",   "2.3",       "Yes", "Yes", "Yes", "Yes", "Yes"))

compute_optimized = (
("Instance Type", "vCPU", "Mem (GiB)", "Instance Storage (GiB)", "Networking Performance",  "CPU", "Clock Speed (GHz)", "Intel AVX", "Intel AVX2", "Intel AVX-512", "Intel Turbo", "EBS OPT", "Enhanced Networking"),
("c5.large",     2,  4,    "EBS-Only",         "Up to 10 Gbps", "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5.xlarge",    4,  8,    "EBS-Only",         "Up to 10 Gbps", "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5.2xlarge",   8,  16,   "EBS-Only",         "Up to 10 Gbps", "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5.4xlarge",   16, 32,   "EBS-Only",         "Up to 10 Gpbs", "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5.9xlarge",   36, 72,   "EBS-Only",         "10 Gigabit",    "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5.18xlarge",  72, 144,  "EBS-Only",         "25 Gigabit",    "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5d.large",    2,  4,    "1 x 50 NVMe SSD",  "Up to 10 Gbps", "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5d.xlarge",   4,  8,    "1 x 100 NVMe SSD", "Up to 10 Gbps", "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5d.2xlarge",  8,  16,   "1 x 200 NVMe SSD", "Up to 10 Gbps", "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5d.4xlarge",  16, 32,   "1 x 400 NVMe SSD", "Up to 10 Gbps", "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5d.9xlarge",  36, 72,   "1 x 900 NVMe SSD", "10 Gigabit",    "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c5d.18xlarge", 72, 144,  "2 x 900 NVMe SSD", "25 Gigabit",    "Intel Xeon Platinum",   "3.0", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"),
("c4.large",     2,  3.75, "EBS-Only",         "Moderate",      "Intel Xeon E5-2666 v3", "2.9", "Yes", "Yes", "-",   "Yes", "Yes", "Yes"),
("c4.xlarge",    4,  7.5,  "EBS-Only",         "High",          "Intel Xeon E5-2666 v3", "2.9", "Yes", "Yes", "-",   "Yes", "Yes", "Yes"),
("c4.2xlarge",   8,  15,   "EBS-Only",         "High",          "Intel Xeon E5-2666 v3", "2.9", "Yes", "Yes", "-",   "Yes", "Yes", "Yes"),
("c4.4xlarge",   16, 30,   "EBS-Only",         "High",          "Intel Xeon E5-2666 v3", "2.9", "Yes", "Yes", "-",   "Yes", "Yes", "Yes"),
("c4.8xlarge",   36, 60,   "EBS-Only",         "10 Gigabit",    "Intel Xeon E5-2666 v3", "2.9", "Yes", "Yes", "-",   "Yes", "Yes", "Yes"))

memory_optimized = (
("Instance Type", "vCPU", "Mem (GiB)", "Instance Storage (GiB)", "Networking Performance",  "CPU", "Clock Speed (GHz)", "Intel AVX", "Intel AVX2", "Intel Turbo", "EBS OPT", "Enhanced Networking"),
("x1.16xlarge",  64,  976,   "1 x 1920 SSD", "10 Gigabit",       "Intel Xeon E7-8880 v3", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("x1.32xlarge",  128, 1952,  "2 x 1920 SSD", "25 Gigabit",       "Intel Xeon E7-8880 v3", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("x1e.xlarge",   4,   122,   "1 x 120 SSD",  "Up to 10 Gigabit", "Intel Xeon E7-8880 v3", "2.3", "Yes", "Yes", "No",  "Yes", "Yes"),
("x1e.2xlarge",  8,   244,   "1 x 240 SSD",  "Up to 10 Gigabit", "Intel Xeon E7-8880 v3", "2.3", "Yes", "Yes", "No",  "Yes", "Yes"),
("x1e.4xlarge",  16,  488,   "1 x 480 SSD",  "Up to 10 Gigabit", "Intel Xeon E7-8880 v3", "2.3", "Yes", "Yes", "No",  "Yes", "Yes"),
("x1e.8xlarge",  32,  976,   "1 x 960 SSD",  "Up to 10 Gigabit", "Intel Xeon E7-8880 v3", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("x1e.16xlarge", 64,  1952,  "1 x 1920 SSD", "10 Gigabit",       "Intel Xeon E7-8880 v3", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("x1e.32xlarge", 128, 3904,  "2 x 1920 SSD", "25 Gigabit",       "Intel Xeon E7-8880 v3", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("r4.large",     2,   15.25, "-",            "Up to 10 Gigabit", "Intel Xeon E5-2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("r4.xlarge",    4,   30.5,  "-",            "Up to 10 Gigabit", "Intel Xeon E5-2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("r4.2xlarge",   8,   61,    "-",            "Up to 10 Gigabit", "Intel Xeon E5-2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("r4.4xlarge",   16,  122,   "-",            "Up to 10 Gigabit", "Intel Xeon E5-2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("r4.8xlarge",   32,  244,   "-",            "10 Gigabit",       "Intel Xeon E5-2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("r4.16xlarge",  64,  488,   "-",            "25 Gigabit",       "Intel Xeon E5-2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"))

accelerated_computing = (
("Instance Type", "vCPU", "Mem (GiB)", "Instance Storage (GiB)", "Networking Performance",  "CPU", "Clock Speed (GHz)", "Intel AVX", "Intel AVX2", "Intel Turbo", "EBS OPT", "Enhanced Networking"),
("p3.2xlarge",  8,  61,  "EBS only",    "Up to 10 Gigabit", "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"),
("p3.8xlarge",  32, 244, "EBS only",    "10 Gigabit",       "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"),
("p3.16xlarge", 64, 488, "EBS only",    "25 Gigabit",       "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"),
("p2.xlarge",   4,  61,  "EBS Only",    "High",             "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"),
("p2.8xlarge",  32, 488, "EBS Only",    "10 Gigabit",       "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"),
("p2.16xlarge", 64, 732, "EBS Only",    "25 Gigabit",       "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"),
("g3.4xlarge",  16, 122, "EBS Only",    "Up to 10 Gigabit", "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"),
("g3.8xlarge",  32, 244, "EBS Only",    "10 Gigabit",       "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"),
("g3.16xlarge", 64, 488, "EBS Only",    "25 Gigabit",       "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"),
("f1.2xlarge",  8,  122, "1 X 480 SSD", "Up to 10 Gigabit", "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"),
("f1.16xlarge", 64, 976, "4 x 960",     "25 Gigabit",       "Intel Xeon E5-2686 v4", "2.3 (base) 2.7 (turbo)", "Yes", "Yes", "Yes", "Yes", "Yes"))

storage_optimized = (
("Instance Type", "vCPU", "Mem (GiB)", "Instance Storage (GiB)", "Networking Performance",  "CPU", "Clock Speed (GHz)", "Intel AVX", "Intel AVX2", "Intel Turbo", "EBS OPT", "Enhanced Networking"),
("h1.2xlarge",  8,  32,    "1 x 2,000 HDD",      "Up to 10 Gigabit", "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("h1.4xlarge",  16, 64,    "2 x 2,000 HDD",      "Up to 10 Gigabit", "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("h1.8xlarge",  32, 128,   "4 x 2,000 HDD",      "10 Gigabit",       "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("h1.16xlarge", 64, 256,   "8 x 2,000 HDD",      "25 Gigabit",       "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("i3.large",    2,  15.25, "1 x 475 NVMe SSD",   "Up to 10 Gigabit", "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("i3.xlarge",   4,  30.5,  "1 x 950 NVMe SSD",   "Up to 10 Gigabit", "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("i3.2xlarge",  8,  61,    "1 x 1,900 NVMe SSD", "Up to 10 Gigabit", "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("i3.4xlarge",  16, 122,   "2 x 1,900 NVMe SSD", "Up to 10 Gigabit", "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("i3.8xlarge",  32, 244,   "4 x 1,900 NVMe SSD", "10 Gigabit",       "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("i3.16xlarge", 64, 488,   "8 x 1,900 NVMe SSD", "25 Gigabit",       "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("i3.metal",    72, 512,   "8 x 1,900 NVMe SSD", "25 Gigabit",       "Intel Xeon E5 2686 v4", "2.3", "Yes", "Yes", "Yes", "Yes", "Yes"),
("d2.xlarge",   4,  30.5,  "3 x 2000",           "Moderate",         "Intel Xeon E5-2676 v3", "2.4", "Yes", "Yes", "Yes", "Yes", "Yes"),
("d2.2xlarge",  8,  61,    "6 x 2000",           "High",             "Intel Xeon E5-2676 v3", "2.4", "Yes", "Yes", "Yes", "Yes", "Yes"),
("d2.4xlarge",  16, 122,   "12 x 2000",          "High",             "Intel Xeon E5-2676 v3", "2.4", "Yes", "Yes", "Yes", "Yes", "Yes"),
("d2.8xlarge",  36, 244,   "24 x 2000",          "10 Gigabit",       "Intel Xeon E5-2676 v3", "2.4", "Yes", "Yes", "Yes", "Yes", "Yes"))

ec2_instance_types = (general_purpose,
                      compute_optimized,
                      memory_optimized,
                      accelerated_computing,
                      storage_optimized)
