from conans import ConanFile, CMake, tools
import os
from cmake_utils import cmake_init, cmake_build_debug_release

class Conan(ConanFile):
    name = "gtest"
    version = "1.8.1"
    description = "Google's C++ test framework"
    homepage = "https://github.com/google/googletest"
    license = "BSD-3-Clause"
    url = "https://gitlab.com/ssrobins/conan-" + name
    settings = "os", "compiler", "arch"
    generators = "cmake"
    exports = "cmake_utils.py"
    exports_sources = ["CMakeLists.txt", "global_settings.cmake", "ios.toolchain.cmake"]
    zip_folder_name = "googletest-release-%s" % version
    zip_name = "release-%s.tar.gz" % version
    build_subfolder = "build"
    source_subfolder = "source"

    def source(self):
        tools.download("https://github.com/google/googletest/archive/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder)

    def package(self):
        self.copy("*.h", dst="include/gtest", src=os.path.join(self.source_subfolder, "googletest", "include", "gtest"))
        self.copy("*.h", dst="include/gmock", src=os.path.join(self.source_subfolder, "googlemock", "include", "gmock"))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("build/lib/*.a", dst="lib", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.debug.libs = ["gmockd", "gmock_maind", "gtestd", "gtest_maind"]
        self.cpp_info.release.libs = ["gmock", "gmock_main", "gtest", "gtest_main"]
        self.cpp_info.libs = self.cpp_info.release.libs
        if self.settings.os == "Linux":
            system_libs = ["pthread"]
            self.cpp_info.debug.libs.extend(system_libs)
            self.cpp_info.release.libs.extend(system_libs)
