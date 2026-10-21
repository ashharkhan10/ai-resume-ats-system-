import { describe, expect, it } from "vitest";
import { checkFile, levelClasses, scoreColor } from "./score";

const fakeFile = (name: string, size: number) => ({ name, size }) as File;

describe("scoreColor", () => {
  it("is green, amber or red", () => {
    expect(scoreColor(84)).toContain("good");
    expect(scoreColor(58)).toContain("warn");
    expect(scoreColor(30)).toContain("bad");
  });
});

describe("levelClasses", () => {
  it("makes High red", () => {
    expect(levelClasses("High")).toContain("bad");
  });
});

describe("checkFile", () => {
  it("accepts PDF and DOCX", () => {
    expect(checkFile(fakeFile("cv.pdf", 1000))).toBeNull();
    expect(checkFile(fakeFile("CV.DOCX", 1000))).toBeNull();
  });
  it("rejects other types, empty and big files", () => {
    expect(checkFile(fakeFile("cv.png", 1000))).toMatch(/PDF or DOCX/);
    expect(checkFile(fakeFile("cv.pdf", 0))).toMatch(/empty/);
    expect(checkFile(fakeFile("cv.pdf", 6 * 1024 * 1024))).toMatch(/too big/);
  });
});
