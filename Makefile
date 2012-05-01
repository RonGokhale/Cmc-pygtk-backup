SHELL := /bin/bash
VERSION := cmc-0.4
VER := 0.4
EMAIL := long.jeremie@gmail.com
VER_DIR := os-versions
BUILD := build
SRC_DIR := src
OUT := out
REQUIRED_DIRS := out

all: cmc-10.04-32 cmc-10.04-64 cmc-11.04-32 cmc-11.04-64 cmc-11.10-32 cmc-11.10-64 cmc-12.04-32 cmc-12.04-64
32: cmc-10.04-32 cmc-11.04-32 cmc-11.10-32 cmc-12.04-32
64: cmc-10.04-64 cmc-11.04-64 cmc-11.10-64 cmc-12.04-64

cmc-10.04-32:
	$(shell for x in $(REQUIRED_DIRS); do if [ ! -d $$x ]; then mkdir -p $$x; fi; done)
	@mkdir -p $(BUILD)/$(VERSION)
	@cp -r $(SRC_DIR)/* $(BUILD)/$(VERSION)/
	@cd $(BUILD)/$(VERSION) ; tar czf $(VERSION).tar.gz * ; cd ../../
	@cd $(BUILD)/$(VERSION) ; yes | dh_make -s -e $(EMAIL) -f $(VERSION).tar.gz ; cd ../../
	@find $(BUILD) -maxdepth 1 -type f -iname *orig.tar.gz -exec rm {} +
	@find $(BUILD) -type f -iname *.ex -exec rm {} +
	@find $(BUILD) -type f -iname *.EX -exec rm {} +
	@cp $(VER_DIR)/common/* $(BUILD)/$(VERSION)/debian/
	@cp $(VER_DIR)/$@/control32 $(BUILD)/$(VERSION)/debian/control
	@rm $(BUILD)/$(VERSION)/debian/source/format
	@cd $(BUILD)/$(VERSION) ; debuild --no-tgz-check -d -ai386 ; cd ../../
	@mkdir -p $(OUT)
	@mv $(BUILD)/*.deb $(OUT)/$@-$(VER).deb
	@rm -rf $(BUILD)

cmc-10.04-64:
	$(shell for x in $(REQUIRED_DIRS); do if [ ! -d $$x ]; then mkdir -p $$x; fi; done)
	@mkdir -p $(BUILD)/$(VERSION)
	@cp -r $(SRC_DIR)/* $(BUILD)/$(VERSION)/
	@cd $(BUILD)/$(VERSION) ; tar czf $(VERSION).tar.gz * ; cd ../../
	@cd $(BUILD)/$(VERSION) ; yes | dh_make -s -e $(EMAIL) -f $(VERSION).tar.gz ; cd ../../
	@find $(BUILD) -maxdepth 1 -type f -iname *orig.tar.gz -exec rm {} +
	@find $(BUILD) -type f -iname *.ex -exec rm {} +
	@find $(BUILD) -type f -iname *.EX -exec rm {} +
	@cp $(VER_DIR)/common/* $(BUILD)/$(VERSION)/debian/
	@cp $(VER_DIR)/$@/control64 $(BUILD)/$(VERSION)/debian/control
	@rm $(BUILD)/$(VERSION)/debian/source/format
	@cd $(BUILD)/$(VERSION) ; debuild --no-tgz-check -d ; cd ../../
	@mkdir -p $(OUT)
	@mv $(BUILD)/*.deb $(OUT)/$@-v$(VER).deb
	@rm -rf $(BUILD)

cmc-11.04-32:
	$(shell for x in $(REQUIRED_DIRS); do if [ ! -d $$x ]; then mkdir -p $$x; fi; done)
	@mkdir -p $(BUILD)/$(VERSION)
	@cp -r $(SRC_DIR)/* $(BUILD)/$(VERSION)/
	@cd $(BUILD)/$(VERSION) ; tar czf $(VERSION).tar.gz * ; cd ../../
	@cd $(BUILD)/$(VERSION) ; yes | dh_make -s -e $(EMAIL) -f $(VERSION).tar.gz ; cd ../../
	@find $(BUILD) -maxdepth 1 -type f -iname *orig.tar.gz -exec rm {} +
	@find $(BUILD) -type f -iname *.ex -exec rm {} +
	@find $(BUILD) -type f -iname *.EX -exec rm {} +
	@cp $(VER_DIR)/common/* $(BUILD)/$(VERSION)/debian/
	@cp $(VER_DIR)/$@/control32 $(BUILD)/$(VERSION)/debian/control
	@rm $(BUILD)/$(VERSION)/debian/source/format
	@cd $(BUILD)/$(VERSION) ; debuild --no-tgz-check -d -ai386 ; cd ../../
	@mkdir -p $(OUT)
	@mv $(BUILD)/*.deb $(OUT)/$@-v$(VER).deb
	@rm -rf $(BUILD)

cmc-11.04-64:
	$(shell for x in $(REQUIRED_DIRS); do if [ ! -d $$x ]; then mkdir -p $$x; fi; done)
	@mkdir -p $(BUILD)/$(VERSION)
	@cp -r $(SRC_DIR)/* $(BUILD)/$(VERSION)/
	@cd $(BUILD)/$(VERSION) ; tar czf $(VERSION).tar.gz * ; cd ../../
	@cd $(BUILD)/$(VERSION) ; yes | dh_make -s -e $(EMAIL) -f $(VERSION).tar.gz ; cd ../../
	@find $(BUILD) -maxdepth 1 -type f -iname *orig.tar.gz -exec rm {} +
	@find $(BUILD) -type f -iname *.ex -exec rm {} +
	@find $(BUILD) -type f -iname *.EX -exec rm {} +
	@cp $(VER_DIR)/common/* $(BUILD)/$(VERSION)/debian/
	@cp $(VER_DIR)/$@/control64 $(BUILD)/$(VERSION)/debian/control
	@rm $(BUILD)/$(VERSION)/debian/source/format
	@cd $(BUILD)/$(VERSION) ; debuild --no-tgz-check -d ; cd ../../
	@mkdir -p $(OUT)
	@mv $(BUILD)/*.deb $(OUT)/$@-v$(VER).deb
	@rm -rf $(BUILD)

cmc-11.10-32:
	$(shell for x in $(REQUIRED_DIRS); do if [ ! -d $$x ]; then mkdir -p $$x; fi; done)
	@mkdir -p $(BUILD)/$(VERSION)
	@cp -r $(SRC_DIR)/* $(BUILD)/$(VERSION)/
	@cd $(BUILD)/$(VERSION) ; tar czf $(VERSION).tar.gz * ; cd ../../
	@cd $(BUILD)/$(VERSION) ; yes | dh_make -s -e $(EMAIL) -f $(VERSION).tar.gz ; cd ../../
	@find $(BUILD) -maxdepth 1 -type f -iname *orig.tar.gz -exec rm {} +
	@find $(BUILD) -type f -iname *.ex -exec rm {} +
	@find $(BUILD) -type f -iname *.EX -exec rm {} +
	@cp $(VER_DIR)/common/* $(BUILD)/$(VERSION)/debian/
	@cp $(VER_DIR)/$@/control32 $(BUILD)/$(VERSION)/debian/control
	@rm $(BUILD)/$(VERSION)/debian/source/format
	@cd $(BUILD)/$(VERSION) ; debuild --no-tgz-check -d -ai386 ; cd ../../
	@mkdir -p $(OUT)
	@mv $(BUILD)/*.deb $(OUT)/$@-v$(VER).deb
	@rm -rf $(BUILD)

cmc-11.10-64:
	$(shell for x in $(REQUIRED_DIRS); do if [ ! -d $$x ]; then mkdir -p $$x; fi; done)
	@mkdir -p $(BUILD)/$(VERSION)
	@cp -r $(SRC_DIR)/* $(BUILD)/$(VERSION)/
	@cd $(BUILD)/$(VERSION) ; tar czf $(VERSION).tar.gz * ; cd ../../
	@cd $(BUILD)/$(VERSION) ; yes | dh_make -s -e $(EMAIL) -f $(VERSION).tar.gz ; cd ../../
	@find $(BUILD) -maxdepth 1 -type f -iname *orig.tar.gz -exec rm {} +
	@find $(BUILD) -type f -iname *.ex -exec rm {} +
	@find $(BUILD) -type f -iname *.EX -exec rm {} +
	@cp $(VER_DIR)/common/* $(BUILD)/$(VERSION)/debian/
	@cp $(VER_DIR)/$@/control64 $(BUILD)/$(VERSION)/debian/control
	@rm $(BUILD)/$(VERSION)/debian/source/format
	@cd $(BUILD)/$(VERSION) ; debuild --no-tgz-check -d ; cd ../../
	@mkdir -p $(OUT)
	@mv $(BUILD)/*.deb $(OUT)/$@-v$(VER).deb
	@rm -rf $(BUILD)

cmc-12.04-32:
	$(shell for x in $(REQUIRED_DIRS); do if [ ! -d $$x ]; then mkdir -p $$x; fi; done)
	@mkdir -p $(BUILD)/$(VERSION)
	@cp -r $(SRC_DIR)/* $(BUILD)/$(VERSION)/
	@cd $(BUILD)/$(VERSION) ; tar czf $(VERSION).tar.gz * ; cd ../../
	@cd $(BUILD)/$(VERSION) ; yes | dh_make -s -e $(EMAIL) -f $(VERSION).tar.gz ; cd ../../
	@find $(BUILD) -maxdepth 1 -type f -iname *orig.tar.gz -exec rm {} +
	@find $(BUILD) -type f -iname *.ex -exec rm {} +
	@find $(BUILD) -type f -iname *.EX -exec rm {} +
	@cp $(VER_DIR)/common/* $(BUILD)/$(VERSION)/debian/
	@cp $(VER_DIR)/$@/control32 $(BUILD)/$(VERSION)/debian/control
	@rm $(BUILD)/$(VERSION)/debian/source/format
	@cd $(BUILD)/$(VERSION) ; debuild --no-tgz-check -d -ai386 ; cd ../../
	@mkdir -p $(OUT)
	@mv $(BUILD)/*.deb $(OUT)/$@-v$(VER).deb
	@rm -rf $(BUILD)

cmc-12.04-64:
	$(shell for x in $(REQUIRED_DIRS); do if [ ! -d $$x ]; then mkdir -p $$x; fi; done)
	@mkdir -p $(BUILD)/$(VERSION)
	@cp -r $(SRC_DIR)/* $(BUILD)/$(VERSION)/
	@cd $(BUILD)/$(VERSION) ; tar czf $(VERSION).tar.gz * ; cd ../../
	@cd $(BUILD)/$(VERSION) ; yes | dh_make -s -e $(EMAIL) -f $(VERSION).tar.gz ; cd ../../
	@find $(BUILD) -maxdepth 1 -type f -iname *orig.tar.gz -exec rm {} +
	@find $(BUILD) -type f -iname *.ex -exec rm {} +
	@find $(BUILD) -type f -iname *.EX -exec rm {} +
	@cp $(VER_DIR)/common/* $(BUILD)/$(VERSION)/debian/
	@cp $(VER_DIR)/$@/control64 $(BUILD)/$(VERSION)/debian/control
	@rm $(BUILD)/$(VERSION)/debian/source/format
	@cd $(BUILD)/$(VERSION) ; debuild --no-tgz-check -d ; cd ../../
	@mkdir -p $(OUT)
	@mv $(BUILD)/*.deb $(OUT)/$@-v$(VER).deb
	@rm -rf $(BUILD)

clean:
	@rm -rf $(OUT)
	@rm -rf $(SRC_DIR)/prog/*.pyc
	@rm -rf $(BUILD)
	@echo Cleaned $(OUT)
