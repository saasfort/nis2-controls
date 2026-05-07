// Package main is a zero-dependency Go CLI lookup tool against the SaaSFort
// NIS2 control library crosswalk.
//
// Usage:
//
//	go run lookup.go "HSTS"
//	go run lookup.go "DKIM records" -framework nis2
//	go run lookup.go -list-checks
//	go run lookup.go -framework bsi -list-controls
//	go run lookup.go -remote "HSTS"
//
// Reads data/check-crosswalk.json from the repo root (relative to this script)
// or from the URL when -remote is passed. Standard library only.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sort"
	"strings"
)

const remoteBase = "https://raw.githubusercontent.com/welcome-archon/nis2-controls/main"

type crosswalkEntry struct {
	Check          string              `json:"check"`
	Controls       map[string][]string `json:"controls"`
	FrameworkCount int                 `json:"framework_count"`
}

type crosswalkDoc struct {
	Checks []crosswalkEntry `json:"checks"`
}

type frameworkDoc struct {
	Controls []struct {
		Control string `json:"control"`
		Title   string `json:"title"`
	} `json:"controls"`
}

func dataDir() string {
	exe, _ := os.Executable()
	// Walk up: .../examples/go/lookup → repo root → data/
	return filepath.Join(filepath.Dir(exe), "..", "..", "data")
}

// When invoked via `go run`, exe path is in /tmp; fall back to relative path.
func loadFile(name string, remote bool) ([]byte, error) {
	if remote {
		resp, err := http.Get(remoteBase + "/data/" + name)
		if err != nil {
			return nil, err
		}
		defer resp.Body.Close()
		if resp.StatusCode != 200 {
			return nil, fmt.Errorf("fetch %s: %d", name, resp.StatusCode)
		}
		return io.ReadAll(resp.Body)
	}
	// Try the executable-relative path first (works for `go build` then run)
	for _, base := range []string{dataDir(), "../../data", "examples/../data"} {
		p := filepath.Join(base, name)
		if data, err := os.ReadFile(p); err == nil {
			return data, nil
		}
	}
	return nil, fmt.Errorf("could not locate %s — try -remote or run from repo root", name)
}

func lookupCheck(needle, framework string, remote bool) error {
	data, err := loadFile("check-crosswalk.json", remote)
	if err != nil {
		return err
	}
	var doc crosswalkDoc
	if err := json.Unmarshal(data, &doc); err != nil {
		return err
	}
	needle = strings.ToLower(needle)
	matched := 0
	for _, c := range doc.Checks {
		if !strings.Contains(strings.ToLower(c.Check), needle) {
			continue
		}
		matched++
		fmt.Printf("\n%s  → %d frameworks\n", c.Check, c.FrameworkCount)
		slugs := []string{"nis2", "iso27001", "bsi", "cis-v8", "nist-csf-v2", "dora", "owasp-asvs-v4"}
		if framework != "" {
			slugs = []string{framework}
		}
		for _, s := range slugs {
			if ctrls, ok := c.Controls[s]; ok && len(ctrls) > 0 {
				fmt.Printf("  %-12s: %s\n", s, strings.Join(ctrls, ", "))
			}
		}
	}
	if matched == 0 {
		return fmt.Errorf("no checks matching %q", needle)
	}
	return nil
}

func listChecks(remote bool) error {
	data, err := loadFile("check-crosswalk.json", remote)
	if err != nil {
		return err
	}
	var doc crosswalkDoc
	if err := json.Unmarshal(data, &doc); err != nil {
		return err
	}
	names := make([]string, 0, len(doc.Checks))
	for _, c := range doc.Checks {
		names = append(names, c.Check)
	}
	sort.Strings(names)
	for _, n := range names {
		fmt.Println(n)
	}
	return nil
}

func listControls(framework string, remote bool) error {
	files := map[string]string{
		"nis2":        "nis2-controls.json",
		"iso27001":    "iso27001-mapping.json",
		"bsi":         "bsi-it-grundschutz-mapping.json",
		"cis-v8":      "cis-v8-mapping.json",
		"nist-csf-v2": "nist-csf-v2-mapping.json",
		"dora":          "dora-mapping.json",
		"owasp-asvs-v4": "owasp-asvs-v4-mapping.json",
	}
	fname, ok := files[framework]
	if !ok {
		return fmt.Errorf("unknown framework: %s", framework)
	}
	data, err := loadFile(fname, remote)
	if err != nil {
		return err
	}
	var doc frameworkDoc
	if err := json.Unmarshal(data, &doc); err != nil {
		return err
	}
	for _, c := range doc.Controls {
		fmt.Printf("%-28s  %s\n", c.Control, c.Title)
	}
	return nil
}

func main() {
	var (
		framework     = flag.String("framework", "", "filter or list mode by framework (nis2|iso27001|bsi|cis-v8|nist-csf-v2)")
		listChecksFl  = flag.Bool("list-checks", false, "print all unique check names")
		listCtrlsFl   = flag.Bool("list-controls", false, "print all controls for -framework")
		remote        = flag.Bool("remote", false, "fetch from raw.githubusercontent.com instead of local data/")
	)
	flag.Parse()
	args := flag.Args()

	var err error
	switch {
	case *listChecksFl:
		err = listChecks(*remote)
	case *listCtrlsFl:
		if *framework == "" {
			fmt.Fprintln(os.Stderr, "-list-controls requires -framework")
			os.Exit(2)
		}
		err = listControls(*framework, *remote)
	case len(args) > 0:
		err = lookupCheck(args[0], *framework, *remote)
	default:
		flag.Usage()
		os.Exit(1)
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}
