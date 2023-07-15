import java.util.Scanner;

class Compound {
  public String atom;
  public float x, y, z;
  Compound(String atom, float x, float y, float z) {
    this.atom = atom;
    this.x = x;
    this.y = y;
    this.z = z;
  }
  void draw() {
    pushMatrix();
    noStroke();
    translate(y * 50, z * 50, x * 50);
    if (atom.equals("H")) {
      fill(0, 0, 255, 128);
    } else if (atom.equals("C")) {
      fill(255, 0, 0, 128);
    } else if (atom.equals("Cl")) {
      fill(255, 255, 0, 128);
    } else if (atom.equals("O")) {
      fill(0, 255, 255, 128);
    } else if (atom.equals("P")) {
      fill(0, 255, 0, 128);
    } else if (atom.equals("N")) {
      fill(255, 0, 255, 128);
    } else {
      fill(255, 255, 255, 128);
    }
    sphere(20);
    popMatrix();
  }
}

Compound[] compounds;
int[][] bonds;

String name;

void setup() {
  size(500, 500, P3D);
  background(0);
  noFill();
  stroke(255);
  strokeWeight(2);
  start();
}

void draw() {
  background(0);

  translate(width/2, height/2);
  fill(255);
  textSize(20);
  textAlign(CENTER);
  text(name, 0, 30-height/2);
  rotateY(frameCount / 200.0);
  rotateX(PI/6.0);
//  stroke(255);
//  strokeWeight(2);
//  noFill();
//  box(300);

  for (Compound c : compounds) {
    c.draw();
  }
  
  stroke(255);
  for (int[] b : bonds) {
    strokeWeight(6);
    if (b[2] == 1) {
      stroke(255, 255, 255);
    } else if (b[2] == 2) {
      stroke(255, 255, 0);
    } else if (b[2] == 3) {
      stroke(255, 0, 255);
    }
    Compound c1 = compounds[b[0]];
    Compound c2 = compounds[b[1]];
    line(c1.y * 50, c1.z * 50, c1.x * 50, c2.y * 50, c2.z * 50, c2.x * 50);
  }
}

void start() {
  try {
    Scanner sc = new Scanner(new File(dataPath("compound.txt")));
    String searchName = sc.nextLine().split(":")[1];
    String cid = sc.nextLine().split(":")[1];
    String cname = sc.nextLine().split(":")[1];
    String smiles = sc.nextLine().split(":")[1];
    name = searchName;
    println(searchName, cid, cname, smiles);
  
    for (int i = 0; i < 3; i++) {
      sc.nextLine();
    }
    int n = sc.nextInt();
    compounds = new Compound[n];
    int m = sc.nextInt();
    bonds = new int[m][3];
    sc.nextLine();
    for (int i = 0; i < n; i++) {
      float x = (float)sc.nextDouble();
      float y = (float)sc.nextDouble();
      float z = (float)sc.nextDouble();
      String atom = sc.next();
      compounds[i] = new Compound(atom, x, y, z);
      sc.nextLine();
    }
    for (int i = 0; i < m; i++) {
      bonds[i][0] = sc.nextInt()-1;
      bonds[i][1] = sc.nextInt()-1;
      bonds[i][2] = sc.nextInt();
      sc.nextLine();
    }
  } catch (IOException e) {
    e.printStackTrace();
  }
}
